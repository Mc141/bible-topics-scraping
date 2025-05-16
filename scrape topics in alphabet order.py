import requests
from bs4 import BeautifulSoup
import csv



letters = []

for i in range(97, 123):
    letters.append("{:c}".format(i))


themes = []

for letter in letters:
    theme_list = []
    
    URL =f'https://www.openbible.info/topics/{letter}'

    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    containers = soup.find_all('ol')



    for list in containers:
        for item in list.find_all('a'):
            theme_list.append(item.text)
        
    theme = {
        f'{letter}': theme_list
    }

    themes.append(theme)




with open('alphabetical_themes.csv', 'w') as csvfile:
    headers = ['letter', 'themes']
    writer = csv.writer(csvfile,delimiter=',', lineterminator='\n')
    writer.writerow(headers)
    
    for entry in themes:
        for letter, theme_list in entry.items():
            writer.writerow([letter, str(theme_list)])