import requests
import json
import csv

def fetch_matriklar_data():
    api_base_url = "https://gis.us.fo/arcgis/rest/services/matriklar/us_matr/MapServer/0/query"

    params = {
        'f': 'json',
        'where': 'cadastral_district_no IN (54,55)',
        'returnGeometry': 'false',
        'spatialRel': 'esriSpatialRelIntersects',
        'outFields': '*',
        'orderByFields': 'OBJECTID ASC',
        'resultOffset': 0,
        'resultRecordCount': 25
    }

    response = requests.get(api_base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'features' in data:
            field_names = data['fields']
            field_aliases = [field['alias'] for field in field_names]
            features = data['features']

            csv_data = []
            for feature in features:
                attributes = feature['attributes']
                row = [attributes.get(field['name'], 'N/A') for field in field_names]
                csv_data.append(row)

            with open('matriklar.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(field_aliases)
                csvwriter.writerows(csv_data)

            print("matriklar.csv has been written.")
        else:
            print("No features found in the response.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
