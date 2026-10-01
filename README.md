# Local Business Lead Extractor & Filtering Pipeline

An automated data extraction and enrichment tool built with Python, Playwright, and Pandas. It extracts business intelligence from local map searches, parses unstructured card layouts, and filters high-intent leads based on contactability and social proof.

## Architecture & Features

- **Dynamic Headless Scraping**: Uses Playwright to handle infinite-scroll feeds and asynchronous rendering.
- **Robust Text Parsing**: Regular expressions extract phone numbers, business ratings, review counts, categories, and website presence from unformatted text cards.
- **Data Enrichment & Deduplication**: Pandas pipeline drops duplicate business records and filters out businesses without phone numbers or website channels.
- **Interactive Segmentation**: CLI prompts allow selecting specific business niches dynamically before exporting shortlist sets.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone [https://github.com/shasvathsk/Lead-Extractor.git](https://github.com/shasvathsk/Lead-Extractor.git)
   cd playwright-lead-extractor