import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def scrape_owner_data():
    """
    
    The function:
    1. Reads parcel data from matriklar.csv
    2. For each parcel, visits its detail page and extracts owner information
    3. Handles rate limiting and retries
    4. Combines original data with owner information
    5. Saves the enriched data to matriklar_with_owners.csv
    
    Returns:
        None
    
    Output:
        Creates/overwrites matriklar_with_owners.csv in the current directory
    """
    # Configure Chrome in non-headless mode for debugging
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Define input and output files
    input_csv = 'matriklar.csv'
    output_csv = 'matriklar_with_owners.csv'
    data = []

    # Read the input CSV and prepare headers for the output
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
        headers.append('Owners')
        headers.append('Registration Dates')
        for row in csvreader:
            data.append(row)

    def scrape_owner(url, max_retries=3):
        """
        Scrapes owner information from a single parcel's detail page.
        
        Args:
            url (str): The URL of the parcel's detail page
            max_retries (int): Maximum number of retry attempts for rate limiting
            
        Returns:
            tuple: (owners, dates) - Comma-separated strings of owner names and registration dates
        """
        attempts = 0
        while attempts < max_retries:
            try:
                print(f"Scraping URL: {url}")
                driver.get(url)

                # Wait for the response div to load (up to 30 seconds)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "response"))
                )

                # Poll for owner information to appear (up to 10 attempts)
                for _ in range(10):
                    response_div = driver.find_element(By.CLASS_NAME, 'response')
                    if "Eigari:" in response_div.get_attribute('innerHTML'):
                        break
                    time.sleep(2)

                response_div = driver.find_element(By.CLASS_NAME, 'response')
                final_content = response_div.get_attribute('innerHTML')
                print("Final response div content:", final_content)

                # Handle rate limiting or reCAPTCHA
                if "score-threshold-not-met" in final_content:
                    print(f"Rate limit or reCAPTCHA issue encountered for {url}. Retrying...")
                    attempts += 1
                    time.sleep(30)
                    continue

                try:
                    # Extract owner information from the table rows
                    owner_rows = response_div.find_elements(By.XPATH, "//strong[contains(text(), 'Eigari:')]/../../following-sibling::tr")
                    owner_names = []
                    owner_dates = []
                    for row in owner_rows:
                        name = row.find_element(By.XPATH, "./td[1]/p").text.strip()
                        date = row.find_element(By.XPATH, "./td[2]/p").text.strip()
                        owner_names.append(name)
                        owner_dates.append(date)

                    owners = ", ".join(owner_names)
                    dates = ", ".join(owner_dates)
                    print(f"Owners found: {owners}")
                    print(f"Registration dates: {dates}")
                    return owners, dates
                except NoSuchElementException:
                    print(f"Owner information not found in {url}")
                    return 'N/A', 'N/A'
            except TimeoutException:
                print(f"Timeout while waiting for {url}")
                return 'N/A', 'N/A'
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
                return 'N/A', 'N/A'
        print(f"Failed to retrieve data from {url} after {max_retries} attempts.")
        return 'N/A', 'N/A'

    # Process each parcel in the dataset
    for index, row in enumerate(data):
        url = row[21]  # URL is in the 22nd column (0-based index)
        print(f"Processing row {index+1}/{len(data)}")
        owners, dates = scrape_owner(url)
        row.append(owners)
        row.append(dates)
        time.sleep(5)  # Rate limiting delay between requests

    # Write the enriched data to the output CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(data)

    print("Updated data with owners has been written to", output_csv)
    driver.quit()
