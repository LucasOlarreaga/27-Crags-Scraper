import requests, sqlite3, json
from bs4 import BeautifulSoup
import time, random, re
from Get_Premium_Locations import clean_response, extract_list, insert_crag_data


# Extract links from the HTML content
def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/crags/') and a['href'] != '/crags/new']
    return links

# Get the URL for the next page
def get_next_page_url(soup):
    next_button = soup.find('li', class_='next')
    if next_button and 'disabled' not in next_button.get('class', []):
        next_link = next_button.find('a', class_='next')
        if next_link:
            return next_link['href']
    return None

# Insert a crag into the database
def wait():
     # Sleep for a random interval between 1 and 7 seconds
    sleep_time = random.uniform(1, 7)
    time.sleep(sleep_time)

# Extract boulders from the HTML content
def extract_boulders(html_content):
    soup = BeautifulSoup(html_content.text, 'html.parser')
    boulders = []

    for row in soup.find_all('tr'):
        name_tag = row.find('a', href=True)
        grade_tag = row.find('span', class_='grade')
        rating_tag = row.find('div', class_='rating')
        votes_tag = row.find('span', class_='stars')
        type_tag = row.find('div', class_='visible-xs-block')
        sector_tag = row.find('a', href=True)
        description_tag = row.find('div', class_='route-block')

        # Workaround way of obtaining ascents through the votes_tag
        ascents = None
        if votes_tag and 'title' in votes_tag.attrs:
            votes_text = votes_tag['title']
            ascents = int(re.search(r'\d+', votes_text).group())
        

        # Check if all the tags are found
        if name_tag and grade_tag and rating_tag and ascents is not None and type_tag and sector_tag and description_tag:
            
            name = name_tag.text.strip().replace('\u2019', "'")
            grade = grade_tag.text.strip()
            rating = float(rating_tag.text.strip())
            type_ = type_tag.text.strip().split()[1]
            sector = sector_tag.text.strip().replace('\u2019', "'")
            description = re.sub(r'\s+', ' ', description_tag.text.strip().replace('\u2019', "'"))
            url = 'https://27crags.com' + name_tag['href']
            
            

            # Append the boulder to the list
            boulders.append({
                'name': name,
                'grade': grade,
                'rating': rating,
                'ascents': ascents,
                'type': type_,
                'sector': sector,
                'description': description,
                'url': url
            })
    return boulders

# Create the database
def create_database():
    conn = sqlite3.connect('files/free_climbs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS boulders (
            url TEXT PRIMARY KEY,
            name TEXT,
            grade TEXT,
            rating REAL,
            ascents INTEGER,
            type TEXT,
            sector TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert boulders into the database
def insert_boulders_into_db(boulders):
    conn = sqlite3.connect('files/free_climbs.db')
    c = conn.cursor()
    for boulder in boulders:
        try:
                c.execute('''
                INSERT INTO boulders (url, name, grade, rating, ascents, type, sector, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (boulder['url'], boulder['name'], boulder['grade'], boulder['rating'], boulder['ascents'], boulder['type'], boulder['sector'], boulder['description']))
        except sqlite3.IntegrityError:
                pass
                print(f"Boulder {boulder['name']} at {boulder['sector']} already exists. Skipping insertion.")    
    conn.commit()
    conn.close()


# Main function
def main():

    country = 'ireland'
    
    # Base URL and current page URL
    base_url = 'https://27crags.com'
    current_page_url = f'/countries/{country.lower()}/descending/by/favourite_count/page/1'
    
    # Where we store the crag links
    crags_links = []
    
    # Failures for printing at end (since we don't break on failure)
    country_failures = []
    crag_failures = []

    # Loop through all the pages
    while current_page_url:
        response = requests.get(base_url + current_page_url)
        if response.status_code != 200:
            print(f"Error: {response.status_code} for URL {current_page_url}")
            country_failures.append(base_url + current_page_url)

        else:
            # Extract the last part of the URL
            last_part = current_page_url.rstrip('/').split('/')[-1]
            print(f"Scraping {country} page {last_part}")
            
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

    # Print the number of crags found once all crags for coutry found
    print(f"Found {len(crags_links)} crags")


    # Create the database
    create_database()

    for index, link in enumerate(crags_links):
        response = requests.request("GET", base_url + link + '/routelist')
        if response.status_code != 200:
            print(f"Error: {response.status_code} for URL {base_url + link + '/routelist'}")
            crag_failures.append(base_url + link + '/routelist')
        else:
            # Extract crag name of the URL
            last_part = link.rstrip('/').split('/')[-1]
            print(f"{index}/{len(crags_links)}) Scraping {last_part}")
            
            # Parse the HTML content using BeautifulSoup
            routes_html = extract_boulders(response)
            insert_boulders_into_db(routes_html)
        wait()


    print(f"Country Failures: {country_failures}")
    print(f"Crag Failures: {crag_failures}")


  
if __name__ == "__main__":
    main()