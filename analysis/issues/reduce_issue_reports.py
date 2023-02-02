# It aggregates all issue reports

import csv
import glob
import sys

csv.field_size_limit(sys.maxsize)

# The position of the component field
COMPONENT_FIELD_POS = 13

# Issues' path
PATH = './data'

def to_cnes_key(name):
    to_hiphen = [' ', '’', '(', ')']
    for c in to_hiphen:
        name = name.replace(c, '_')
    name = name.replace(':', '-')
    # If there is a slash, get the first part (for compatibility with the module that clones the repos)
    return name.split('/')[0]

sonar_keys = []

# Reading repos
with open(
    "../../scraping/repo_list/data/awesome_ml_mv.csv",
    "r",
    encoding="utf-8",
    newline="",
) as f:
    reader = csv.reader(f, dialect="unix")
    next(reader)

    for row in reader:
        sonar_keys.append(to_cnes_key(row[1]))


def get_project_issues(filename):
    python_issues = []

    with open(
        filename,
        "r",
        encoding="utf-8",
        newline="",
    ) as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)

        for row in reader:
            python_issues.append(row)
        
    return python_issues

issues = []

for key in sonar_keys:
    filename = list(glob.iglob(f"data/*{key}*.csv"))
    if len(filename) > 0:
        print(f"Collecting issues from {filename[0]} \n")
        issues.extend(get_project_issues(filename[0]))

fieldnames = [
    'severity', 
    'updateDate', 
    'comments', 
    'line', 
    'author', 
    'rule',	
    'project', 
    'effort', 
    'message', 
    'creationDate', 
    'type', 
    'quickFixAvailable',
    'tags', 
    'component', 
    'flows', 
    'scope', 
    'textRange', 
    'debt', 
    'key', 
    'hash', 
    'status'
]

with open('data/issues.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, dialect='excel')
    writer.writerow(fieldnames)
    writer.writerows(issues)
