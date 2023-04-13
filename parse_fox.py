import csv
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time


retry_strategy = Retry(total=5, backoff_factor=2)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)

# Read in the CSV file with the article information
with open('positive.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    rows = list(reader)

# Define the output file header
output_header = ['title', 'url', 'publication_date', 'contains_fl_data_background']

# Open the output CSV file for writing
with open('articles_with_fl_data_background.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(output_header)

    # Loop through each article and check if it contains the fl-data-background class
    for row in rows:
        # Combine the base URL with the article URL
        url = 'https://www.foxnews.com' + row[1]

        # Make a request to the article URL
        try:
            response = http.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f'Error requesting URL: {url} {e}')
            continue

        # Parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
        import pdb;pdb.set_trace()

        # Check if the page contains the fl-data-background class
        contains_fl_data_background = bool(soup.find('g', class_='fl-data-background'))

        # Add a row to the output CSV file
        output_row = [row[0], row[1], row[2], contains_fl_data_background]
        writer.writerow(output_row)

        time.sleep(2)