import pandas as pd

df = pd.read_csv("leads.csv")
df = df.drop_duplicates(subset=["name", "phone"])

# Get category counts, then turn them into a numbered list
category_counts = df["category"].value_counts()
category_list = category_counts.index.tolist()  # just the category names, in order

print("Categories found in your results:\n")
for i, cat in enumerate(category_list, start=1):
    print(f"{i}. {cat} ({category_counts[cat]})")

keep_input = input("\nEnter the NUMBERS of categories to KEEP, separated by commas: ")
selected_numbers = [int(n.strip()) for n in keep_input.split(",")]

# Convert chosen numbers back into actual category names
keep_list = [category_list[n - 1] for n in selected_numbers]
print(f"\nKeeping: {keep_list}")

df = df[df["category"].isin(keep_list)]

df = df[(df["phone"].notna() & (df["phone"] != "")) |
        (df["has_website"] == "Yes")]

df["reviews"] = pd.to_numeric(df["reviews"], errors="coerce").fillna(0)
df = df.sort_values(by=["reviews"], ascending=False)

print(f"\nFiltered down to {len(df)} usable leads")
df.to_csv("leads_filtered.csv", index=False)
df.head(25).to_csv("leads_shortlist.csv", index=False)
print("Saved top 25 to leads_shortlist.csv")