import requests
from bs4 import BeautifulSoup

URL = 'https://www.openbible.info/topics/a_healthy_marriage'

r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')


container = soup.find('form', attrs={'id': 'vote'})

verses = []

for item in container.find_all('a', attrs = {'class':'bibleref'}):
    verses.append(item.text)
    
print(verses)