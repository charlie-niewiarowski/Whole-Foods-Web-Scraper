# Whole Foods Web Scraper
A Python-based web scraper that extracts product listings from the Whole Foods website, including item names, brands, and prices.

## Features
- Scrapes all products for a given Whole Foods store ID
- Parses:
  - Product `id`
  - Product name
  - Brand
  - Product slug
  - Price
  - Image links
  - Unit of measure
  - Availability flags (e.g. `isLocal`)
- Saves data as a `.csv` file

## Deps
- `requests` for HTTP API access
- `csv` for output file creation
- Python 3
