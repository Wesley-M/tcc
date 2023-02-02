"""
It uses the CNES Report sonarqube plugin to generate issue reports
for all repositories
"""

import csv
import os


def to_sonar_key(name):
    """ Converts a name to a sonar key compatible one """
    to_hiphen = [' ', '’', '(', ')']
    for c in to_hiphen:
        name = name.replace(c, '_')
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
        sonar_keys.append(to_sonar_key(row[1]))

i = 0
for key in sonar_keys:
    print(f"[ {round((i+1) * 100 / len(sonar_keys), 2)}% ] Generating report of {key}... \n")
    os.system(f"java -jar sonar-cnes-report-4.1.2.jar -m -e -w -o ./data -p {key}")
    print("---")  
    i += 1
