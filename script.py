import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://help.wincloudpms.com"
visited_links = set()
faq_data = []

def scrape_page(url):
    print(f"Scraping {url}")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Adjust this based on the HTML structure
    question_elements = soup.find_all("h1")  # Replace with actual Q selector
    answer_elements = soup.find_all("div", class_="article-body")  # Replace with A selector
    
    if question_elements and answer_elements:
        for q, a in zip(question_elements, answer_elements):
            faq_data.append({
                "question": q.text.strip(),
                "answer": a.get_text(strip=True)
            })

    # Follow internal links to explore deeper pages
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/") and (BASE_URL + href) not in visited_links:
            full_url = BASE_URL + href
            visited_links.add(full_url)
            time.sleep(1)
            scrape_page(full_url)

# Kick off the scrape
scrape_page(BASE_URL)

# Save to JSON
with open("wincloud_faq.json", "w") as f:
    json.dump(faq_data, f, indent=2)
