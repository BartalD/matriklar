import requests
import json
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Base API URL
api_base_url = "https://gis.us.fo/arcgis/rest/services/matriklar/us_matr/MapServer/0/query"

# Parameters for API request
params = {
    'f': 'json',
    'where': 'cadastral_district_no IN (54,55)', # Sí readme fyri bygdanummar
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields': '*',
    'orderByFields': 'OBJECTID ASC',
    'resultOffset': 0, # Hvar røðin byrjar - Tvs. at hetta skal incrementast við 'resultRecordCount' hvørja ferð
    'resultRecordCount': 25 # Hvussu nógv verður tikið í senn
}

# API request
response = requests.get(api_base_url, params=params)

if response.status_code == 200:
    data = response.json()
    
    if 'features' in data:
        field_names = data['fields']
        field_aliases = [field['alias'] for field in field_names]
        features = data['features']
        
        # CSV
        csv_data = []
        for feature in features:
            attributes = feature['attributes']
            row = [attributes.get(field['name'], 'N/A') for field in field_names]
            csv_data.append(row)
        
        # Write
        with open('matriklar.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Header
            csvwriter.writerow(field_aliases)
            # Data
            csvwriter.writerows(csv_data)
        
        print("Data has been written successfully.")
    else:
        print("No features found in the response.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    
    
    
#######################
# Owner Scraping      #
#######################


# Function to scrape owner information from URL
def scrape_owner(url):
    try:
        print(f"Scraping URL: {url}")
        driver.get(url)
        
        # Wait for the initial response div to appear
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "response"))
        )
        
        # Wait for the dynamic content to be loaded into the response div
        max_attempts = 10
        for attempt in range(max_attempts):
            response_div = driver.find_element(By.CLASS_NAME, 'response')
            if "Eigari:" in response_div.get_attribute('innerHTML'):
                break
            time.sleep(2)  # Wait a bit before trying again
        
        response_div = driver.find_element(By.CLASS_NAME, 'response')
        print("Final response div content:", response_div.get_attribute('innerHTML'))
        
        try:
            # Locate the 'Eigari:' text and find the owner information
            owner_td = response_div.find_element(By.XPATH, "//strong[contains(text(), 'Eigari:')]")
            owner_name = owner_td.find_element(By.XPATH, '../../following-sibling::tr[1]/td/p').text.strip()
            print(f"Owner found: {owner_name}")
            return owner_name
        except NoSuchElementException:
            print(f"Owner information not found in {url}")
            print("Response div content:", response_div.get_attribute('innerHTML'))
            return 'N/A'
    except TimeoutException:
        print(f"Timeout while waiting for {url}")
        return 'N/A'
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return 'N/A'

# Selenium WebDriver
options = Options()
options.headless = False  # Set to False for debugging
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Reading existing CSV data
input_csv = 'matriklar.csv'
output_csv = 'matriklar_with_owners.csv'
data = []

with open(input_csv, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)
    headers.append('Owner')  # Add new column for owners
    for row in csvreader:
        data.append(row)

# Updating data with owners
for index, row in enumerate(data):
    url = row[21]  # Assuming the URL is in the 22nd column
    print(f"Processing row {index+1}/{len(data)}")
    owner = scrape_owner(url)
    row.append(owner)
    time.sleep(1)  # Delay to avoid hitting the server too frequently

# Writing updated data to new CSV file
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)
    csvwriter.writerows(data)

print("Updated data with owners has been written to", output_csv)

# Closing the WebDriver
driver.quit()
