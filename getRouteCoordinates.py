import requests
import re
import json
import csv

def get_cragmap(crag_name):
    url = f"https://27crags.com/crags/{crag_name}/cragmap"
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_cragmap_json(crag_data):

    # Extract the GoogleMap JSON from the script
    match = re.search(r'GoogleMap\((\{.*?\})\);', crag_data, re.DOTALL)
    if not match:
        raise Exception("Could not find GoogleMap JSON in file.")

    data = json.loads(match.group(1))

    rows = []

    # Extract boulders
    for b in data.get("boulders", []):
        rows.append({
            "type": "boulder",
            "name_or_info": b.get("name", ""),
            "latitude": b.get("latitude", ""),
            "longitude": b.get("longitude", ""),
            "url": b.get("url", "")
        })

    # Extract map_markers
    for m in data.get("map_markers", []):
        rows.append({
            "type": m.get("kind", "marker"),
            "name_or_info": m.get("info", ""),
            "latitude": m.get("latitude", ""),
            "longitude": m.get("longitude", ""),
            "url": m.get("url", "")
        })

    # Write to CSV
    with open("fionnay_locations.csv", "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["type", "name_or_info", "latitude", "longitude", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print("Extraction complete. See fionnay_locations.csv")

# Example usage:
if __name__ == "__main__":
    crag_name = "fionnay"  # Change this to any crag name
    data = get_cragmap(crag_name)
    get_cragmap_json(data)