from playwright.sync_api import sync_playwright
import re
import csv

def parse_card(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    data = {"name": "", "rating": "", "reviews": "", "category": "",
            "address": "", "phone": "", "has_website": "No"}
    if not lines:
        return data
    data["name"] = lines[0]

    rating_pattern = re.compile(r"^(\d\.\d)\((\d[\d,]*)\)$")
    phone_pattern = re.compile(r"(\+?\d[\d\s]{7,}\d)")
    price_pattern = re.compile(r"^[₹$]\s?\d")
    hours_keywords = ("Open", "Closed")

    category_found = False
    for line in lines[1:]:
        if line == data["name"]:
            continue

        m = rating_pattern.match(line)
        if m:
            data["rating"] = m.group(1)
            data["reviews"] = m.group(2).replace(",", "")
            continue
        if line == "No reviews":
            data["rating"], data["reviews"] = "N/A", "0"
            continue
        if line == "Website":
            data["has_website"] = "Yes"
            continue
        if line == "Directions":
            continue

        if line.startswith(hours_keywords):
            phone_match = phone_pattern.search(line)
            if phone_match:
                data["phone"] = phone_match.group(1).strip()
            continue

        if not category_found:
            parts = [p.strip() for p in line.split("·") if p.strip()]
            data["category"] = parts[0]
            for part in parts[1:]:
                if not price_pattern.match(part):
                    data["address"] = part
            category_found = True
            continue

        phone_match = phone_pattern.search(line)
        if phone_match and not data["phone"]:
            data["phone"] = phone_match.group(1).strip()

    return data

search = input("enter what to search: ")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.google.com/maps")
    page.wait_for_timeout(10000)
    page.fill("input#ucc-1", search)
    page.press("input", "Enter")

    page.wait_for_selector(".Nv2PK", timeout=10000)
    page.screenshot(path="debug.png", full_page=True)
    feed = page.locator('div[role="feed"]')
    previous_count = 0
    while True:
        results = page.locator(".Nv2PK").all()
        current_count = len(results)
        print(f"So far: {current_count} results")

        if current_count == previous_count:
            break

        previous_count = current_count
        feed.hover()
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(5000)

    print(f"Final total: {len(results)} results")

    leads = []
    for result in results:
        parsed = parse_card(result.inner_text())
        leads.append(parsed)

    with open("leads.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "rating", "reviews",
                                                 "category", "address", "phone", "has_website"])
        writer.writeheader()
        writer.writerows(leads)

    print(f"Saved {len(leads)} leads to leads.csv")

    browser.close()