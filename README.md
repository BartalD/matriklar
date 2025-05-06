# 🗺️ Matriklar Scraper

A Python project that fetches Faroese land registry (matriklar) data from the public GIS API and enriches it with owner information via web scraping. Built for clean reproducibility using [`uv`](https://github.com/astral-sh/uv) for dependency and environment management.

---

## 📦 Features

- Fetches cadastral parcel data from [https://gis.us.fo](https://gis.us.fo)
- Parses and stores parcel data in `matriklar.csv`
- Uses Selenium to extract detailed owner information
- Produces a full `matriklar_with_owners.csv` dataset
- CLI options to run individual steps
- Fully managed Python environment via `uv`

---

## 🚀 Quickstart

### Prerequisites

- Python 3.8 or higher
- Git
- pipx (for installing uv)

### 1. Install uv

First, install `uv` using pipx:

```bash
pipx install uv
```

### 2. Clone and Set Up the Project

```bash
# Clone the repository
git clone https://github.com/BartalD/matriklar.git
cd matriklar

# Create and activate virtual environment
uv venv

# Install dependencies from pyproject.toml
uv pip install .
```

## ▶️ Usage

The project can be run in different modes depending on your needs:

```bash
# Run the complete pipeline (fetch and scrape)
uv run -- python main.py

# Only fetch the cadastral data
uv run -- python main.py --step fetch

# Only scrape owner information
uv run -- python main.py --step scrape
```

### Output Files

- `matriklar.csv`: Contains the raw cadastral data
- `matriklar_with_owners.csv`: Contains the enriched data with owner information

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
