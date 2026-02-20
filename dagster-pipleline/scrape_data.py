import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Scrape specific data (e.g., articles, product data, etc.)
        data = []
        articles = soup.find_all("div", class_="article")
        for article in articles:
            title = article.find("h2").get_text()
            date = article.find("time").get_text()
            data.append({"title": title, "date": date})

        return data
    else:
        raise Exception(f"Failed to scrape data from {url}")
