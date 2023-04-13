import csv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

url = "https://www.foxnews.com/api/article-search?searchBy=contributor&value=content%2Ffnc%2Fperson%2Fc%2Femma-colton&size=30&sort=published_desc&from={}"
retry_strategy = Retry(total=5, backoff_factor=2)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

from_param = 0
articles = []
while True:
    current_url = url.format(from_param)
    response = http.get(current_url, headers=headers)
    if not response.ok:
        print(f"Failed to retrieve articles from {current_url} with status code {response.status_code}")
        continue

    data = response.json()
    if not data:
        print(f"No more articles found at {current_url}")
        break

    articles.extend(data)
    from_param += 30
    time.sleep(2)

# Create CSV
with open("fox_news_articles.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["title", "link", "date"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for article in articles:
        writer.writerow({
            "title": article["title"],
            "link": article["url"],
            "date": article["publicationDate"],
        })
print(f"Saved {len(articles)} articles to fox_news_articles.csv")
