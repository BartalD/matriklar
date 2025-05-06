# 🗺️ Matriklar Scraper

A Python project that fetches Faroese land registry (matriklar) data from the public GIS API and enriches it with owner information via web scraping. Built for clean reproducibility using [`uv`](https://github.com/astral-sh/uv) for dependency and environment management.

---

## 📦 Features

- Fetches cadastral parcel data from [https://gis.us.fo](https://gis.us.fo)
- Parses and stores parcel data in `matriklar.csv`
- Uses Selenium to extract detailed owner info
- Produces a full `matriklar_with_owners.csv` dataset
- CLI options to run individual steps
- Fully managed Python environment via `uv`

---

## 🚀 Quickstart

### 1. Install [uv](https://github.com/astral-sh/uv)

`pipx install uv`

### 2. Set up the project

```
git clone https://github.com/YOUR_USERNAME/matriklar.git
cd matriklar
uv venv
uv pip install -r requirements.txt  # if you have a lockfile, or...
uv add requests selenium webdriver-manager
```

## ▶️ Usage

`uv run -- python main.py [--step fetch|scrape|all]`

### Examples:

- `uv run -- python main.py`
- `uv run -- python main.py --step fetch`
- `uv run -- python main.py --step scrape`
