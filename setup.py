"""
This file clones all repositories in the awesome ml list for local analysis, and
ensures that only the project visible folders are in there.
"""

import csv
import glob
import os

awesome_list = []

CATEG = 0
NAME = 1
LINK = 2
DESC = 3

# It dictates the project in which the clone operation will start
start_at = 0

# The list of ml projects to consider
REPO_LIST_PATH = "scraping/repo_list/data/awesome_ml_mv.csv"

with open(REPO_LIST_PATH, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f, dialect='unix')
    
    # headers: ['category', 'name', 'link', 'description']
    next(reader)

    for row in reader:
        awesome_list.append(row)

print("Starting to clone repositories in :repos")

progress = start_at
for i, repo in enumerate(awesome_list):
    if (i >= start_at - 1):
        repo_name = repo[NAME]
        if (len(repo[NAME].split()) > 1):
            repo_name = repo[NAME].replace(" ", "_")
        
        if not os.path.isdir("./repos/{}".format(repo_name)):
            print("\n[{}] Cloning {} ...".format(progress, repo[LINK]))
            print("git clone {} \"./repos/{}\"".format(repo[LINK], repo_name))
            os.system("git clone {} \"./repos/{}\"".format(repo[LINK], repo_name))
            print("Done")

        progress += 1


# ------------------------------------------------------------
# Removing old folders, that are not being analysed anymore.

print("\nRemoving old repos: ")

awesome_list_repo_names = [x[NAME].replace(" ", "_").split("/")[0] for x in awesome_list]

for repo_path in glob.iglob('repos/*'):
    if repo_path.split('/')[1] not in awesome_list_repo_names:
        print('--------------------')
        print(f'{repo_path} - You shouldnt be here!')
        print('Removing...')
        os.system(f'rm -rf {repo_path}')
        print('[OK]')
