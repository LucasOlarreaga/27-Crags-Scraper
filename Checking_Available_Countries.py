import csv
import requests
import time
import random
from Get_Free_Locations import wait
    
# Base URL and current page URL
base_url = 'https://27crags.com'

# Failures for printing at end (since we don't break on failure)
country_failures = []
country_success = []

# Read countries from CSV file
countries = []
# Country file comes from: https://github.com/bnokoro/Data-Science/blob/master/countries%20of%20the%20world.csv
# Did some manual modifications for easier reading
with open('files/countries.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        countries.append(row[0])

# Loop through all the pages
for country in countries:
    country_cleaned = country.rstrip().replace(" ", "-").lower()
    print(f"Scraping '{country_cleaned}'")
    current_page_url = f'/countries/{country_cleaned}/descending/by/favourite_count/page/1'
    response = requests.get(base_url + current_page_url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} for URL {current_page_url}")
        country_failures.append(base_url + current_page_url)
    else:
        print(f"Scraped {country_cleaned} page 1")
        country_success.append(country_cleaned)
    wait()

print(f"Successes: {len(country_success)}")

# Print failures
if len(country_failures) > 0:
       # Write failures to CSV file
    with open('/Users/lolarreaga/Documents/GitHub/theCragScrap/files/country_failures.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL'])
        for url in country_failures:
            writer.writerow([url])
