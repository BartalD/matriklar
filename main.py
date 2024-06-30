import requests
import json
import csv

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