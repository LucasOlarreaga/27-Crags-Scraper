import requests, json, sqlite3
from bs4 import BeautifulSoup
import time, random

# Makes an API call to 27crags
def api_call(location_id):
    url = f"https://27crags.com/areas/{location_id}/routelist?order_by=rating_desc&system=French,Font,French"
    payload = {}
    headers = {}

    return requests.request("GET", url, headers=headers, data=payload)

# Response from API call has lxml and many different elements we don't want (we just want the JSON data)
def clean_response(response):
    soup = BeautifulSoup(response.text, 'lxml')
    script_tags = soup.find_all('script', type='application/json', attrs={'data-component-name': ['Nav', 'RouteList']})
    # Extracting the JSON data from the script tags
    json_elements = []
    for script_tag in script_tags:
        try:
            json_data = json.loads(script_tag.string)
            json_elements.append(json_data)
        except json.JSONDecodeError:
            continue
    return json_elements

# Extracts the json list from the Dictionnary data
def extract_list(json_data):
    routes = []
    for key, element in json_data.items():
        if isinstance(element, list):
            if key == 'routes' or key == 'areas':  # Combine conditions for clarity
                routes.extend(element)
        elif isinstance(element, str) and "static/appicons" in element:
            continue  # Skip elements containing ".png"
        else:
            print(f"Unexpected element type: {type(element)}, element: {element}")  # Debug print
    return routes

# Create a database to store the crag data
def create_db():
    conn = sqlite3.connect('files/free_climbs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS crags
                 (id TEXT PRIMARY KEY, name TEXT, genre TEXT, grade_int TEXT, param_id TEXT, rating REAL,
                  ascents_done_count TEXT, video_count TEXT, discussion_count TEXT, crimpers TEXT,
                  slopers TEXT, jugs TEXT, fingery TEXT, powerful TEXT, dyno TEXT, endurance TEXT,
                  technical TEXT, mental TEXT, roof TEXT, overhang TEXT, vertical TEXT, slab TEXT,
                  traverse TEXT, sitstart TEXT, topslasthold TEXT, tradgear_required TEXT, dangerous TEXT,
                  crack TEXT, pockets TEXT, tufas TEXT, crag_name TEXT, crag_param_id TEXT, country TEXT, region TEXT)''')
    conn.commit()
    return conn, c

# Insert crag data into the database
def insert_crag_data(c, crag_data, location):
    for index, crag in enumerate(crag_data):
        if isinstance(crag, dict):
            try:
                c.execute('''INSERT INTO crags (id, name, genre, grade_int, param_id, rating, ascents_done_count, video_count, discussion_count, crimpers, slopers, jugs, fingery, powerful, dyno, endurance, technical, mental, roof, overhang, vertical, slab, traverse, sitstart, topslasthold, tradgear_required, dangerous, crack, pockets, tufas, crag_name, crag_param_id, country, region)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (crag.get('id'), crag.get('name'), crag.get('genre'), crag.get('grade_int'), crag.get('param_id'), crag.get('rating'), crag.get('ascents_done_count'), crag.get('video_count'), crag.get('discussion_count'), crag.get('crimpers'), crag.get('slopers'), crag.get('jugs'), crag.get('fingery'), crag.get('powerful'), crag.get('dyno'), crag.get('endurance'), crag.get('technical'), crag.get('mental'), crag.get('roof'), crag.get('overhang'), crag.get('vertical'), crag.get('slab'), crag.get('traverse'), crag.get('sitstart'), crag.get('topslasthold'), crag.get('tradgear_required'), crag.get('dangerous'), crag.get('crack'), crag.get('pockets'), crag.get('tufas'), crag.get('crag_name'), crag.get('crag_param_id'), location.get('country'), location.get('name')))
            except sqlite3.IntegrityError:
                pass
                print(f"Record with id {crag.get('id')} already exists ({crag.get('name')}). Skipping insertion.")
        else:
            print(f"Unexpected element type at index {index}: {type(crag)} - Value: {crag}")

def main():
    # Create a connection to the database
    conn, c = create_db()

    # Location ID of an initial random crag to get location list from the 27crags API
    location_id = 1801

    # Making the API call
    response = api_call(location_id)

    # Checking if the response is valid
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        
    # Only getting the JSON out of the lxml response
    json_elements = clean_response(response)

    # Separating the JSON dictionnaries
    locations_json = json_elements[0] if len(json_elements) > 0 else None

    # Getting a list of routes from the JSON dictionnaries
    location_list = extract_list(locations_json)  

    # Loop through each location in the location list
    for index, location in enumerate(location_list):
        param_id = location.get('param_id')
        if param_id:
            # Make an API call with the param_id
            response = api_call(param_id)
            if response.status_code == 200:
                # Clean the response to get JSON data
                json_elements = clean_response(response)
                crag_json = json_elements[1] if len(json_elements) > 1 else None
                if crag_json:
                    # Extract the list from the dict data within the JSON
                    crag_list = extract_list(crag_json)
                    
                    # Insert the crag data into the database
                    insert_crag_data(c, crag_list, location)
            else:
                print(f"Error: {response.status_code} for location id {param_id}")
        print(f"{index}/{len(location_list)}) Location {location.get('name')} in {location.get('country')} is done")
        
        # Sleep for a random interval between 1 and 7 seconds
        sleep_time = random.uniform(1, 7)
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
        print("Done sleeping!")

    conn.commit()
    conn.close()
    print("Done!")
   

if __name__ == "__main__":
    main()

