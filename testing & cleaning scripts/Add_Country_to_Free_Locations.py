import requests, sqlite3
from bs4 import BeautifulSoup
import csv, sys, os

# Add the directory containing Get_Free_Locations.py to the sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

# Import functions from Get_Free_Locations.py
from Get_Free_Locations import extract_links, get_next_page_url, wait


# This script is to update the database schema and add the country information to the boulders
# This is because the initial script was already ran over a long period of time, and to avoid having
# to re-run the entire script, and go through an api call for each crag again

# Add a country column to the database
def update_database_schema():
    conn = sqlite3.connect('files/free_climbs.db')
    c = conn.cursor()
    try:
        c.execute('''
            ALTER TABLE boulders ADD COLUMN country TEXT
        ''')
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e):
            print("Column 'country' already exists.")
        else:
            raise
    conn.commit()
    conn.close()

# Update the boulders with the country
def update_boulders_with_country(crags_links, country):
    conn = sqlite3.connect('files/free_climbs.db')
    c = conn.cursor()
    for link in crags_links:
        url = 'https://27crags.com' + link
        c.execute('''
            UPDATE boulders
            SET country = ?
            WHERE url LIKE ?
        ''', (country, url + '%'))
    conn.commit()
    conn.close()


# Main function
def main():

    # Failures for printing at end (since we don't break on failure)
    country_failures = []
    crag_failures = []

    # Read countries from CSV file
    countries = []

    # Country file comes from: https://github.com/bnokoro/Data-Science/blob/master/countries%20of%20the%20world.csv
    # Did some manual modifications for easier reading
    
    # Read countries from CSV file
    with open('files/countries.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            countries.append(row[0])

    # Update the database schema
    update_database_schema()

    for country in countries:
    
        # Base URL and current page URL
        base_url = 'https://27crags.com'
        country_cleaned = country.rstrip().replace(" ", "-").lower()
        current_page_url = f'/countries/{country_cleaned}/descending/by/favourite_count/page/1'
        
        # Where we store the crag links
        crags_links = []

        # Loop through all the pages
        while current_page_url:
            response = requests.get(base_url + current_page_url)
            if response.status_code != 200:
                print(f"Error: {response.status_code} for URL {current_page_url}")
                country_failures.append(base_url + current_page_url)

            else:
                # Extract the last part of the URL
                last_part = current_page_url.rstrip('/').split('/')[-1]
                print(f"Scraping {country}page {last_part}")
                
                # Parse the HTML content using BeautifulSoup
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extract links from the current page
                links = extract_links(html_content)
                crags_links.extend(links)

                # Get the URL for the next page
                current_page_url = get_next_page_url(soup)

            # Sleep for a random interval 
            wait()

        # Update the existing records with the country information
        update_boulders_with_country(crags_links, country)
        


  
if __name__ == "__main__":
    main()