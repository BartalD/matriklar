import argparse
from data_fetcher import fetch_matriklar_data
from owner_scraper import scrape_owner_data

def main():
    parser = argparse.ArgumentParser(description="Matriklar data tool")
    parser.add_argument(
        "--step",
        choices=["fetch", "scrape", "all"],
        default="all",
        help="Which step to run: fetch, scrape, or all (default)",
    )

    args = parser.parse_args()

    if args.step == "fetch":
        fetch_matriklar_data()
    elif args.step == "scrape":
        scrape_owner_data()
    else:  # args.step == "all"
        fetch_matriklar_data()
        scrape_owner_data()

if __name__ == "__main__":
    main()
