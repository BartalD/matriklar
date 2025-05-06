import requests
import json
import csv

def fetch_matriklar_data():
    """
    Fetches ALL cadastral data from the Faroese GIS API using pagination
    and writes the results to matriklar.csv.
    """
    api_base_url = "https://gis.us.fo/arcgis/rest/services/matriklar/us_matr/MapServer/0/query"
    batch_size = 2000
    offset = 0
    all_features = []
    field_names = []
    field_aliases = []

    print("Fetching all cadastral data...")

    while True:
        print(f"Fetching records {offset}–{offset + batch_size - 1}...")
        params = {
            'f': 'json',
            'where': '1=1',
            'returnGeometry': 'false',
            'spatialRel': 'esriSpatialRelIntersects',
            'outFields': '*',
            'orderByFields': 'OBJECTID ASC',
            'resultOffset': offset,
            'resultRecordCount': batch_size
        }

        response = requests.get(api_base_url, params=params)

        if response.status_code != 200:
            print(f"Request failed at offset {offset}. Status code: {response.status_code}")
            break

        data = response.json()

        if offset == 0:
            # Only extract field metadata once
            if 'fields' in data:
                field_names = data['fields']
                field_aliases = [field['alias'] for field in field_names]
            else:
                print("Missing field definitions in response.")
                return

        features = data.get('features', [])
        if not features:
            print("No more features returned.")
            break

        all_features.extend(features)

        if len(features) < batch_size:
            print("Final batch received.")
            break

        offset += batch_size

    # Write to CSV
    csv_data = []
    for feature in all_features:
        attributes = feature['attributes']
        row = [attributes.get(field['name'], 'N/A') for field in field_names]
        csv_data.append(row)

    with open('matriklar.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(field_aliases)
        writer.writerows(csv_data)

    print(f"✅ Wrote {len(csv_data)} records to matriklar.csv.")
