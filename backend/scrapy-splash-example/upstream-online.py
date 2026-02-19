import requests
import json
from bs4 import BeautifulSoup

url = "http://localhost:8050/render.html"

payload = json.dumps({
  "url": "https://www.upstreamonline.com/field-development/chinese-contractor-in-210-million-deal-to-revamp-africa-gas-field/2-1-1703068" # page URL to render
})
headers = {
  'content-type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')
# Find the div containing the news content
content_div = soup.find('div', class_='dn-content')

if content_div:
# Extract the text from all <p> tags within the div
    paragraphs = content_div.find_all('p')
    news_content = ' '.join([p.get_text() for p in paragraphs])
    print(news_content)
