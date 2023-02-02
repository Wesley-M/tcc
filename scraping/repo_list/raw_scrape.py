"""
It roughly scrapes the list on github
"""

import csv

import requests
from bs4 import BeautifulSoup

REPO_URL = "https://github.com/josephmisiti/awesome-machine-learning"

REPO_HTML = requests.get(REPO_URL)

PARSED_REPO_CONTENT = BeautifulSoup(REPO_HTML.content, "html.parser")

# All the 'a' tags preceding the machine learning sections
python_sections_a = PARSED_REPO_CONTENT.findAll('a', attrs={ 
    'name': lambda x: x and x.startswith('user-content-python-') 
})

awesome_list = []

for section_a in python_sections_a:
    # The section content
    section = section_a.findNext('ul')
    
    # Each li from the section
    for li in section.findAll('li'):
        awesome_list.append({
            'category': section_a.findNext('h4').get_text(),
            'name': li.find('a').get_text(),
            'link': li.find('a')['href'],
            'description': li.get_text()
        })

# CSV file header
fieldnames = ['category', 'name', 'link', 'description']

# open the file in write mode
with open('data/awesome_ml.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='unix')
    writer.writeheader()
    writer.writerows(awesome_list)
