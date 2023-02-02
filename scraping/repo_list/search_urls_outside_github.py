"""
It identifies all the listed repos with links pointing outside of github
"""

import csv
import json
import re

awesome_list = []
unknown = []

# Constants
constants_f = open('../../config/constants.json')
constants = json.load(constants_f)

HEADER = constants["AWESOME_HEADER_ENUM"]

with open('data/awesome_ml.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f, dialect='unix')
    
    # headers: ['category', 'name', 'link', 'description']
    next(reader)

    for row in reader:
        awesome_list.append(row)

# Catching all the urls that don't match the pattern: https://github.com
for repo in awesome_list:
    if (re.match("https://github.com", repo[HEADER["LINK"]]) == None):
        unknown.append([repo[HEADER["NAME"]], repo[HEADER["LINK"]]])

# open the file in write mode
with open('data/unknown_repos.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, dialect='unix')
    
    # write the header
    writer.writerow(["name", "link"])

    # write multiple rows
    writer.writerows(unknown)
