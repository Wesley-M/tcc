import csv
import datetime
import os
import re
import subprocess

import requests
from requests.auth import HTTPBasicAuth

# First, start sonarqube with local 'sonar' user: /opt/sonarqube/bin/linux-x86-64/sonar.sh console

# The api to manage the sonarqube instance
SONAR_WEB_API = 'http://localhost:9000/api/'

# https://docs.sonarqube.org/latest/user-guide/metric-definitions/
TO_COLLECT = [
    'ncloc',
    'ncloc_language_distribution',
    'complexity',
    'duplicated_lines_density',
    'cognitive_complexity',
    'code_smells',
    'sqale_rating', # Maintainability Rating
    'sqale_index', # technical debt
    'bugs', # number of bugs
    'violations', # Issues
    'reliability_rating',
    'vulnerabilities',
    'security_rating',
    'alert_status',
    'reliability_remediation_effort'
]

CATEG = 0
NAME = 1
LINK = 2
DESC = 3

repos = []
result = []

# Projects analysed till this threshold will be ignored
TIME_THRESHOLD = 12 * 60 * 60 * 99999 # 12 hours in seconds 

def to_sonar_key(name):
    """ Converts a name to a sonar key compatible one """
    to_hiphen = [' ', '’', '(', ')']
    for c in to_hiphen:
        name = name.replace(c, '_')
    # If there is a slash, get the first part (for compatibility with the module that clones the repos)
    return name.split('/')[0]


# If flattens the array of metrics of a project in a python dict
def flatten_metrics(metrics):
    metrics_dict = {}
    for metric in metrics:
        metrics_dict[metric['metric']] = metric['value']
    return metrics_dict


# Collects project metrics
def collect_proj_metrics(name):
    req = requests.get('{}measures/component?metricKeys={}&component={}'.format(SONAR_WEB_API, ','.join(TO_COLLECT), name))
    try:
        metrics = req.json()['component']['measures']
    except:
        print("***")
        print(req.json())
        print("***")
        raise Exception("Error")
    return flatten_metrics(metrics)


# Reading repos
with open(
    "../../scraping/repo_list/data/awesome_ml_mv.csv",
    "r",
    encoding="utf-8",
    newline="",
) as f:
    reader = csv.reader(f, dialect="unix")

    # headers: ['category', 'name', 'link', 'description']
    next(reader)

    for row in reader:
        repos.append(
            {
                "name": row[NAME],
                "type": row[CATEG],
                "fullname": re.search('https://github.com/(.*)$', row[LINK]).group(1).rstrip('/'),
            }
        )


# READING REPO NAMES THAT DIDNT RUN IN PREVIOUS RUNS

anomalies = []

with open(
    "./data/anomalies.csv",
    "r",
    encoding="utf-8",
    newline="\n",
) as f:
    reader = csv.reader(f, dialect="unix")

    next(reader)
    for row in reader:
        anomalies.append(to_sonar_key(row[0]))


# ANALYSING REPOS ONE BY ONE

i = 0
for repo in repos:
    repo_name = repo['name'].replace(' ', '_')

    # Creating config file in repo folder
    with open(os.path.join('../../repos/{}'.format(repo_name), 'sonar-project.properties'), 'w') as temp_file:
        exists = requests.post(SONAR_WEB_API + 'projects/search?projects={}'.format(repo_name), 
            auth=HTTPBasicAuth("3b1aec1c9a20e71c28b631653fe60cdab858be80", ""))

        sonar_key = to_sonar_key(repo_name)

        print("---")
        print(f"{round(i * 100 / len(repos), 2)}% - [Project: <{sonar_key}>]")
        
        components = exists.json()['components']

        # Project was not analyzed yet
        if len(components) != 0 or (components and components[0]['lastAnalysisDate']):
            currProject = components[0]

            # Check the date of the last analysis
            if 'lastAnalysisDate' in currProject and currProject['lastAnalysisDate']:
                validDate = "-".join(currProject['lastAnalysisDate'].split("-")[:-1])
                lastDate = datetime.datetime.fromisoformat(validDate)
                timePassed = (datetime.datetime.now() - lastDate).total_seconds()

                print(f"Last analysis: {lastDate}")
                print(f"How many time has passed: {timePassed}")
                
                # If the threshold is bigger or equal to the time passed, go to the next
                if not timePassed > TIME_THRESHOLD:
                    repo = {**repo, **collect_proj_metrics(sonar_key)}
                    result.append(repo)
                    i += 1
                    continue

            temp_file.write(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', """
                # must be unique in a given SonarQube instance
                sonar.projectKey={}

                # --- optional properties ---

                # defaults to project key
                #sonar.projectName=My project
                # defaults to 'not provided'
                #sonar.projectVersion=1.0
                
                # Path is relative to the sonar-project.properties file. Defaults to .
                #sonar.sources=.
                
                # Encoding of the source code. Default is default system encoding
                #sonar.sourceEncoding=UTF-8
            """.format(sonar_key), flags=re.M))

            print("Created settings file")

            # Create sonarqube project
            project_req = requests.post(SONAR_WEB_API + 'projects/create?name={}&project={}'.format(sonar_key, sonar_key))

            print("Created project {}".format(repo_name))

            # Running sonarqube analysis 
            subprocess.run([
                "sonar-scanner",
                '-Dsonar.projectKey={}'.format(sonar_key),
                '-Dsonar.host.url=http://localhost:9000',
                '-Dsonar.projectBaseDir=../repos/{}'.format(repo_name),
                '-Dsonar.sources=.',
                '-Dsonar.inclusions=**/*.py',
                '-Dsonar.login=3b1aec1c9a20e71c28b631653fe60cdab858be80'
            ])

            print("Ran analysis for {}".format(repo_name))

            print("---")

        repo = {**repo, **collect_proj_metrics(sonar_key)}
        result.append(repo)

        i += 1

print(result)

# CSV file header
fieldnames = ['name', 'type', 'fullname']
fieldnames.extend(TO_COLLECT)

# open the file in write mode
with open('data/repo_qube_stats.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='unix')
    writer.writeheader()
    writer.writerows(result)


