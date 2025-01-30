import csv, requests
import pandas as pd
from bs4 import BeautifulSoup


# Getting the subset of crags that have routes from the crags_data.csv file
def get_subset_crag_df():
    # Define the file path
    csv_file_path = '/Users/lolarreaga/Documents/GitHub/theCragScrap/files/crags_data.csv'

    # Create an empty DataFrame
    crags_df = pd.DataFrame(columns=['name', 'param_id', 'latitude', 'longitude', 'routes_count'])

    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # Iterate through the rows in the CSV file
        for row in csv_reader:
            # Create a DataFrame for the current row
            row_df = pd.DataFrame([{
                'name': row['name'],
                'param_id': row['param_id'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'routes_count': row['route_count']
            }])
            
            # Concatenate the current row DataFrame with the main DataFrame
            crags_df = pd.concat([crags_df, row_df], ignore_index=True)

    # Filter the DataFrame to include only rows where 'routes_count' is greater than 0
    crags_df = crags_df[crags_df['routes_count'].astype(int) > 0]   

    return crags_df


# Getting the routes from each crag
def get_routes_from_crags(crags_df):

    # Initialize a list to hold the data
    bouldering_routes = []

    # Iterate through the crags
    for index, crag in crags_df.iterrows():
        
        # Extract the 'param_id' from the current crag
        param_id = crag['param_id']

        # Make a request to the crag's route list page
        print(f"{index}/{len(crags_df)}) Getting routes for crag {crag['name']}")
        response = requests.get(f'https://27crags.com/crags/{param_id}/routelist')
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <tr> elements
        for tr in soup.find_all('tr'):
            # Extracting route name
            name_div = tr.find('div', class_='hidden')
            if not name_div:
                continue
            route_name = name_div.text.strip()

            # Extracting grade
            grade_div = tr.find('span', class_='grade')
            route_grade = grade_div.text.strip() if grade_div else 'N/A'

            # Extracting type
            type_td = tr.find_all('td', class_='hidden-xs')[1]
            route_type = type_td.text.strip() if type_td else 'N/A'

            # Extracting ascents (from the <td> with class 'hidden-xs' and integer content)
            ascents_count = '0'
            for td in tr.find_all('td', class_='hidden-xs'):
                text = td.text.strip()
                if text.isdigit():
                    ascents_count = text
                    break

            # Extracting location
            location_div = tr.find('div', class_='visible-xs-block')
            if location_div:
                location_links = location_div.find_all('a')
                location_link = location_links[0].text.strip() if location_links else 'N/A'
            else:
                location_link = 'N/A'

            # Extracting rating
            rating_div = tr.find('div', class_='rating')
            route_rating = rating_div.text.strip() if rating_div else '0.0'

            # Add the extracted data to the list
            bouldering_routes.append([route_name, route_grade, route_type, ascents_count, location_link, route_rating, crag['name'], crag['latitude'], crag['longitude']])


    return bouldering_routes
    

def main(test=False):

    # Get the subset of crags that have routes
    crags_df = get_subset_crag_df()

    # If test is True, only get the first 4 crags
    if test == True:
        crags_df = crags_df[:4]

    # Get the routes from the crags
    routes_df= get_routes_from_crags(crags_df)

    print('Finished getting routes, now writing to CSV')

    # Write data to CSV
    with open('files/routes_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Route Name', 'Grade', 'Type', 'Ascents', 'Sector', 'Rating', 'Crag Name', 'Latitude', 'Longitude'])  # Header row
        writer.writerows(routes_df)

    print("Data has been written to CSV")

 
if __name__ == '__main__':
    main()