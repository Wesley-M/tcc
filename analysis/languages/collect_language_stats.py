import csv
import json
import os
import re

from dotenv import load_dotenv
from github import Github

# It collects language metadata from the repos

languages_api = "https://api.github.com/repos/{}/{}/languages"
languages_md = {}
total_lines = sum(1 for line in open('../../scraping/repo_list/data/awesome_ml_mv.csv'))

# Github client
load_dotenv()

PERSONAL_TOKEN = os.getenv('PERSONAL_TOKEN')

g = Github(PERSONAL_TOKEN)

# Constants
constants_f = open('../../config/constants.json')
constants = json.load(constants_f)

HEADER = constants["AWESOME_HEADER_ENUM"]

def languages(link):
    """ Returns the languages for a project """
    fullname = re.search("https://github.com/(.*)$", link).group(1).rstrip("/")
    try:
        return g.get_repo(fullname).get_languages()
    except:
        print("Failed on: {}".format(fullname))

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
        print(f'[{round((i+1) * 100 / total_lines, 1)}%] Requesting languages from {owner}/{repo}')
        
        languages_md[row[HEADER["NAME"]]] = languages(row[HEADER["LINK"]])
            
        i += 1

with open('data/languages_metadata.json', 'w', encoding='utf-8') as outfile:
    json.dump(languages_md, outfile)
