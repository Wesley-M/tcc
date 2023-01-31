"""
This script identifies all the listed repos with links pointing outside of github
"""

import csv
import re

awesome_list = []
unknown = []

CATEG = 0
NAME = 1
LINK = 2
DESC = 4

with open('data/awesome_ml.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f, dialect='unix')
    
    # headers: ['category', 'name', 'link', 'description']
    next(reader)

    for row in reader:
        awesome_list.append(row)

# Catching all the urls that don't match the pattern: https://github.com
for repo in awesome_list:
    if (re.match("https://github.com", repo[LINK]) == None):
        unknown.append([repo[NAME], repo[LINK]])

# open the file in the write mode
with open('data/unknown_repos.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, dialect='unix')
    
    # write the header
    writer.writerow(["name", "link"])

    # write multiple rows
    writer.writerows(unknown)
