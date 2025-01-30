import requests, math
from bs4 import BeautifulSoup
import json, pandas as pd


# Define the grade hash for converting grades to a french grade format
grade_hash = {100: "3", 150: "3+", 200: "4", 250: "4+", 275: "4+", 300: "5",
        350: "5+", 370: "5+", 380: "5+", 400: "6A", 450: "6A+",
        500: "6B", 550: "6B+", 575: "6B+", 600: "6C", 650: "6C+",
        700: "7A", 750: "7A+", 800: "7B", 850: "7B+", 900: "7C",
        950: "7C+", 1000: "8A", 1050: "8A+", 1100: "8B", 1150: "8B+",
        1200: "8C", 1250: "8C+", 1300: "9A", 1350: "9A+", 1400: "9B",
        1450: "9B+", 1500: "9C", 1550: "9C+", 1600: "10A", 0: "?"}


# Function to get the list of crags
def get_crags_list(url):

    # Make initial the API call to get list of all crags
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract and filter the data you need in one BeautifulSoup search
    crag_list_data = soup.find('script', type='application/json', class_='js-react-on-rails-component', attrs={'data-component-name': ['Mapbox']})
    data = json.loads(crag_list_data.string)
    df = pd.DataFrame(data['crags'])

    return df


# Function to get the details of each crag (mostly param_id, for routelist)
def get_crag_details(json_content):

    # Initialize a list to hold the data
    updates = []

    # Iterate through the crags
    for crag in json_content['crags']:

        # Extract top-level fields
        crag_data = {
            'id': crag['id'],
            'param_id': crag['param_id'],
            'route_count': crag.get('route_count', 0),
            '3_count': crag.get('grade1_count', 0),
            '4_count': crag.get('grade2_count', 0),
            '5_count': crag.get('grade3_count', 0),
            '5+_count': crag.get('grade4_count', 0),
            '6a_count': crag.get('grade5_count', 0),
            '6b_count': crag.get('grade6_count', 0),
            '6c_count': crag.get('grade7_count', 0),
            '7a_count': crag.get('grade8_count', 0),
            '7b_count': crag.get('grade9_count', 0),
            '7c_count': crag.get('grade10_count', 0),
            '8a_count': crag.get('grade11_count', 0),
            '8b_count': crag.get('grade12_count', 0),
            '8c_count': crag.get('grade13_count', 0),
            '9a_count': crag.get('grade14_count', 0),
            'topo_count': crag.get('topo_count', 0)
        }

        # Extract nested fields
        route_counts = crag['route_counts']
        # Iterate through the different types of route counts (sport, boulder, trad, etc.)
        for route_type, grades in route_counts.items():
            # Convert the route type to a key (name)
            route_type_key = route_type.lower().replace(' ', '_')
            # Iterate through the different grades for a specific route type
            for grade_key, count in grades.items():
                # Convert the hashed grade to font grade used in the key (name)
                grade_name = grade_hash.get(int(grade_key), grade_key)
                # Using the key (name with route type and grade) to store the count
                crag_data[f'{route_type_key}_{grade_name}'] = count

        updates.append(crag_data)

    # Convert updates to DataFrame and merge with the original DataFrame
    updates_df = pd.DataFrame(updates)
    return updates_df


def main(test=False):

    # Get the list of crags
    df = get_crags_list("https://27crags.com/crags")

    # Initialize all_updates_df
    all_updates_df = pd.DataFrame()
    
    # Extract all IDs from the DataFrame and concatenate them into a single string separated by commas
    all_ids = df['id'].astype(str).tolist()
    if test == True:
        all_ids = all_ids[:100]
    len_all_ids = math.ceil(len(all_ids) / 50)

    # Iterate through the IDs in batches of 50 (max limit for the API call)
    while all_ids:

        # Extract the first 50 IDs
        fifty_ids = all_ids[:50]
        # Concatenate the IDs into a single string separated by commas
        concatenated_ids = ','.join(fifty_ids)
        # Remove the first 50 IDs from the list
        all_ids = all_ids[50:]

        print(f'{math.ceil(len(all_ids)/50)}/{len_all_ids} batches of IDs left')

        # Make the API call with the concatenated IDs
        response = requests.get(f'https://27crags.com/api/web01/crags?ids={concatenated_ids}')
        json_content = json.loads(response.text)

        # Get the crag details for the 50 crags of this loop
        updates_df = get_crag_details(json_content)
        # Concatenate the current updates DataFrame with the main updates DataFrame
        all_updates_df = pd.concat([all_updates_df, updates_df], ignore_index=True)

        # Break the loop if there are less than 50 IDs left (last batch)
        if len(fifty_ids) < 50:
            break

    
    # Merge the original DataFrame with all updates
    print('Finished getting crag details, now merging the dataframes')
    df = pd.concat([df.set_index('id'), all_updates_df.set_index('id')], axis=1).reset_index()


    # Convert the DataFrame to a CSV file
    print('Finished merging, now saving to CSV')
    df.to_csv('files/crags_data.csv', index=False, encoding='utf-8')
    print("Saved to csv")


if __name__ == '__main__':
    main()
    print("Finished")


