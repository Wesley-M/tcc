"""
This script tries to find the Github URL for projects with URLs pointing outside Github domain.
For example, some projects point to their's project site, instead of the Github repository.

The results still need to be manually verified, given that we search for the project name on Github,
and assume the project is the first listed.

-- To start, you can run:
python3 collect_github_urls.py

-- If a error occurs, then:
python3 collect_github_urls.py recover
"""

import csv
import json
import os
import re
import sys

from dotenv import load_dotenv
from github import Github

# Constants
constants_f = open('../../utils/constants.json')
constants = json.load(constants_f)

HEADER = constants["AWESOME_HEADER_ENUM"]

# Set it to True if the script failed before when searching for URLs
SCRIPT_FAILED = True if len(sys.argv) > 1 and sys.argv[1] == 'recover' else False

# The output file path
OUTPUT = 'data/awesome_ml_plus_unknown_urls.csv'

# The file from which we will read the repo list. If the script failed by rate limit before,
# then we read the last output file without losing progress.
if SCRIPT_FAILED:
    FILE_TO_READ = OUTPUT
else:
    FILE_TO_READ = 'data/awesome_ml.csv'

awesome_list = []

#########################################################################
# READING REPO LIST AND RECOVERING LOST PROGRESS [SCRIPT WAS INTERRUPTED]
#########################################################################

with open(FILE_TO_READ, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f, dialect='unix')
    
    # headers: ['category', 'name', 'link', 'description']
    next(reader)

    for row in reader:
        awesome_list.append(row)

# Setting the github client

load_dotenv()

PERSONAL_TOKEN = os.getenv('PERSONAL_TOKEN')

g = Github(PERSONAL_TOKEN)

# Swapping unknown urls for Github's urls

def is_from_github(url):
    return re.match("https://github.com", url) != None

regular = 0
for repo in awesome_list:
    if not is_from_github(repo[HEADER["LINK"]]):
        print("{} - {}".format(repo[HEADER["NAME"]], repo[HEADER["LINK"]]))
        possible_repos = g.search_repositories(repo[HEADER["NAME"]])
        try:
            if possible_repos.totalCount > 0:
                print("Repo URL: {}.".format(possible_repos[0].html_url))
                repo[HEADER["LINK"]] = possible_repos[0].html_url
            else:
                print("There was no such repo O.o")
                repo[HEADER["LINK"]] = repo[HEADER["LINK"]]
        except Exception as e:
            print(str(e))
            repo[HEADER["LINK"]] = repo[HEADER["LINK"]]
    else:
        regular += 1

print("{} project(s) failed!".format(len(awesome_list) - regular))

# CSV file header
headers = ['category', 'name', 'link', 'description']

# open the file in the write mode
with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, dialect='unix')
    
    # write the header
    writer.writerow(headers)

    # write multiple rows
    writer.writerows(awesome_list)
