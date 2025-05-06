import requests
import json
import csv

def fetch_matriklar_data():
    """
    Fetches cadastral data from the Faroese GIS API and saves it to matriklar.csv.
    
    The function:
    1. Makes a request to the GIS API for cadastral data
    2. Processes the JSON response
    3. Extracts field names and their aliases
    4. Writes the data to a CSV file with proper headers
    
    Returns:
        None
    
    Output:
        Creates/overwrites matriklar.csv in the current directory
    """
    # Base URL for the Faroese GIS API cadastral data endpoint
    api_base_url = "https://gis.us.fo/arcgis/rest/services/matriklar/us_matr/MapServer/0/query"

    # API request parameters
    params = {
        'f': 'json',                                    # Request JSON format
        'where': 'cadastral_district_no IN (54,55)',    # Filter for specific districts
        'returnGeometry': 'false',                      # Don't include geometry data
        'spatialRel': 'esriSpatialRelIntersects',       # Spatial relationship type
        'outFields': '*',                               # Return all fields
        'orderByFields': 'OBJECTID ASC',                # Sort by object ID
        'resultOffset': 0,                              # Start from first record
        'resultRecordCount': 25                         # Number of records to fetch
    }

    # Make the API request
    response = requests.get(api_base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'features' in data:
            # Extract field information from the API response
            field_names = data['fields']
            field_aliases = [field['alias'] for field in field_names]
            features = data['features']

            # Process each feature and extract its attributes
            csv_data = []
            for feature in features:
                attributes = feature['attributes']
                # Create a row for each feature using field names
                row = [attributes.get(field['name'], 'N/A') for field in field_names]
                csv_data.append(row)

            # Write the data to CSV file
            with open('matriklar.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                # Write headers using field aliases
                csvwriter.writerow(field_aliases)
                # Write all data rows
                csvwriter.writerows(csv_data)

            print("matriklar.csv has been written.")
        else:
            print("No features found in the response.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
