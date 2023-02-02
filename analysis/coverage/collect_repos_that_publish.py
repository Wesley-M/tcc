"""
 It searches and isolates which repositories potentially have coverage in their README.md
"""

import csv
import json
import re

import requests

# Constants
constants_f = open('../../config/constants.json')
constants = json.load(constants_f)

HEADER = constants["AWESOME_HEADER_ENUM"]

TOTAL_LINES = sum(1 for line in open('../../scraping/repo_list/data/awesome_ml_mv.csv'))

README_API = "https://raw.githubusercontent.com/{}/{}/{}/README.{}"


repos_with_coverage = []
readmes = []

def get_readme(owner, repo):
    branches = ['master', 'main']
    extensions = ['rst', 'md']
    
    readme = ""

    for b in branches:
        for e in extensions:
            readme = requests.get(README_API.format(owner, repo, b, e)).text
            if (readme == "404: Not Found"): 
                continue
            else:
                return readme

    return readme

with open(
    "../../scraping/repo_list/data/awesome_ml_mv.csv",
    "r",
    encoding="utf-8",
    newline="",
) as f:
    reader = csv.reader(f, dialect="unix")

    # headers: ['category', 'name', 'link', 'description']
    next(reader)
        
    i = 0
    for row in reader:
        owner, repo = re.search("https://github.com/(.*)$", row[HEADER["LINK"]]).group(1).rstrip("/").split('/')
        
        print('---')
        print(f'[{round((i+1) * 100 / TOTAL_LINES, 1)}%] Requesting README from {owner}/{repo}:')
        
        readme = get_readme(owner, repo).lower()

        if 'cov' in readme:
            repos_with_coverage.append(row[HEADER["NAME"]])
            readmes.append({
                "repo": row[HEADER["NAME"]],
                "content": readme
            })
            print(f'[SUCCESS]')
        else:
            print(f'[ERROR]')

        i += 1


with open('data/repos_with_coverage.csv', 'w', newline='\n') as file:
    file.write('repo\n')
    for r in repos_with_coverage:
        file.write(r)
        file.write('\n')

# CSV file header
fieldnames = ['repo', 'content']

# open the file in write mode
with open('data/readmes_with_cov.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='unix')
    writer.writeheader()
    writer.writerows(readmes)