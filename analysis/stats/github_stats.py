"""
Scraping metrics from Github
"""

import csv
import json
import os
import re
import subprocess
import sys

import requests
from dotenv import load_dotenv
from github import Github

# Constants
constants_f = open('../../config/constants.json')
constants = json.load(constants_f)
HEADER = constants["AWESOME_HEADER_ENUM"]

# Setting the github client
load_dotenv()
PERSONAL_TOKEN = os.getenv('PERSONAL_TOKEN')
g = Github(PERSONAL_TOKEN)

# From which repo to start scraping (It can be used when there was an error during the execution)
START_AT_REPO = 0

repos = []

# READING NAME, TYPE AND LINK OF THE REPOS

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
                "name": row[HEADER["NAME"]],
                "type": row[HEADER["TYPE"]],
                "fullname": re.search("https://github.com/(.*)$", row[HEADER["LINK"]])
                .group(1)
                .rstrip("/"),
            }
        )


# ---- COLLECTING METRICS

def folder_size(path):
    """ Disk usage in megabytes """
    return subprocess.check_output(["du", "-sm", path]).split()[0].decode("utf-8")


def commit_count(fullname):
    """ Requests the number of commits for the repo """
    headers = {"Authorization": "token %s" % PERSONAL_TOKEN}
    return re.search(
        "\d+$",
        requests.get(
            "https://api.github.com/repos/{}/commits?per_page=1".format(fullname),
            headers=headers,
        ).links["last"]["url"],
    ).group()


for curr_pos, repo in enumerate(repos):
    if curr_pos >= START_AT_REPO:
        try:
            curr = g.get_repo(repo["fullname"])
            print(
                ">>> [{}] Requesting metadata from: {}".format(
                    curr_pos, repo["fullname"]
                )
            )

            repo["stars"] = curr.stargazers_count
            repo["forks"] = curr.forks_count
            repo["open-issues"] = curr.open_issues_count
            repo["repo_size"] = folder_size(
                "../../repos/{}".format(repo["name"].replace(" ", "_"))
            )
            repo["commits"] = commit_count(repo["fullname"])

            print("---")
            print(repo)
            print("---")
        except:
            print("Failed on: {}".format(repo["fullname"]), sys.exc_info()[0])


# ---- WRITING METRICS TO FILE

# CSV file header
fieldnames = [
    "name",
    "type",
    "fullname",
    "stars",
    "forks",
    "open-issues",
    "repo_size",
    "commits",
]

# open the file in write mode
with open("data/repos_stats.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, dialect="unix")
    writer.writeheader()
    writer.writerows(repos)
