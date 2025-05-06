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

## 🏘️ Markatalsbygdir

| ID  | Location              | ID  | Location            |
| --- | --------------------- | --- | ------------------- |
| 11  | Sumba                 | 58  | Oyrar               |
| 12  | Vágur                 | 59  | Norðskála           |
| 13  | Nes – Vágur           | 60  | Eiði                |
| 14  | Porkeri               | 61  | Gjógv               |
| 15  | Hov                   | 62  | Funningur           |
| 16  | Fámjin                | 63  | Skála               |
| 17  | Øravík                | 64  | Elduvík             |
| 18  | Trongisvágur          | 65  | Oyndarfjørður       |
| 19  | Froðba                | 66  | Fuglafjørður        |
| 20  | Hvalba                | 67  | Leirvík             |
| 21  | Dímun                 | 68  | Norðragøta          |
| 22  | Skúvoy                | 69  | Gøtugjógv           |
| 23  | Skarvanes             | 70  | Syðrugøta           |
| 24  | Dalur                 | 71  | Søldarfjørður       |
| 25  | Húsavík               | 72  | Lambi               |
| 26  | Skálavík              | 73  | Glyvrar             |
| 27  | Sandur                | 74  | Toftir              |
| 28  | Sandavágur            | 75  | Nes – Eysturoy      |
| 29  | Miðvágur              | 76  | Syðradalur – Kalsoy |
| 30  | Sørvágur              | 77  | Húsar               |
| 31  | Bøur                  | 78  | Mikladalur          |
| 32  | Gásadalur             | 79  | Trøllanes           |
| 33  | Mykines               | 80  | Kunoy               |
| 34  | Koltur                | 81  | Haraldssund         |
| 35  | Hest                  | 82  | Skarð               |
| 36  | Nólsoy                | 83  | Norðoyri            |
| 37  | Kirkjubøur            | 84  | Klaksvík            |
| 38  | Velbastaður           | 85  | Strond              |
| 39  | Syðradalur – Streymoy | 86  | Skálatoftir         |
| 40  | Norðradalur           | 87  | Múli                |
| 41  | Skælingur             | 88  | Depil               |
| 42  | Leynar                | 89  | Norðtoftir          |
| 43  | Kvívík                | 90  | Árnafjørður         |
| 44  | Vestmanna             | 91  | Hvannasund          |
| 45  | Saksun                | 92  | Viðareiði           |
| 46  | Tjørnuvík             | 93  | Svínoy              |
| 47  | Haldarsvík            | 94  | Kirkja              |
| 48  | Streymnes             | 95  | Hattarvík           |
| 49  | Hvalvík               |     |                     |
| 50  | Hósvík                |     |                     |
| 51  | Kollafjørður          |     |                     |
| 52  | Kaldbak               |     |                     |
| 53  | Sund                  |     |                     |
| 54  | Hoyvík                |     |                     |
| 55  | Tórshavn              |     |                     |
| 56  | Strendur              |     |                     |
| 57  | Selatrað              |     |                     |

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
