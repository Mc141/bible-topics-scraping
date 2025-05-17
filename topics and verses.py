import requests
from bs4 import BeautifulSoup
import csv
import time
import json

def fetch_url(url, retries=3, delay=2):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/114.0.0.0 Safari/537.36'
        )
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return None

letters = [chr(i) for i in range(97, 123)]  # a-z
alphabet_themes = []

# Step 1: Scrape themes by letter
for letter in letters:
    URL = f'https://www.openbible.info/topics/{letter}'
    r = fetch_url(URL)
    if not r:
        print(f"Skipping letter '{letter}' due to fetch failure.")
        continue

    soup = BeautifulSoup(r.content, 'html5lib')
    containers = soup.find_all('ol')

    for ol in containers:
        for item in ol.find_all('a'):
            theme = item.text.lower().replace(" ", "_").strip("_")
            alphabet_themes.append({
                'letter': letter,
                'theme': theme
            })
    time.sleep(1)  # polite delay between letter pages

# Step 2: Fetch verses for each theme
for obj in alphabet_themes:
    theme = obj['theme']
    verses = []

    # Fix a known theme mismatch
    if theme == "zoroastrian_priests":
        theme = 'zoroastrian'

    URL = f'https://www.openbible.info/topics/{theme}'
    r = fetch_url(URL)
    if not r:
        print(f"Skipping theme '{theme}' due to fetch failure.")
        obj['verses'] = []
        continue

    soup = BeautifulSoup(r.content, 'html5lib')
    container = soup.find('form', attrs={'id': 'vote'})

    if container:
        for item in container.find_all('a', attrs={'class': 'bibleref'}):
            verses.append(item.text)

    obj['verses'] = verses
    time.sleep(1)  # polite delay between theme pages

# Step 3: Save results to CSV with verses as JSON string
with open('themes_with_verses.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['letter', 'theme', 'verses']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for obj in alphabet_themes:
        writer.writerow({
            'letter': obj['letter'],
            'theme': obj['theme'],
            'verses': json.dumps(obj['verses'])  # store list as JSON string
        })

print("Done! Data saved to 'themes_with_verses.csv'")
