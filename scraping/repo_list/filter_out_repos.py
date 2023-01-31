import csv
import json
import os

# ------------------------------------------------------------------
# It filters out projects that are not able to pass certain filters
# ------------------------------------------------------------------

constants_f = open('../utils/constants.json')
constants = json.load(constants_f)
AWL_HEADER = constants["AWESOME_HEADER_ENUM"]

# Where the filtered results will go
filtered_results_f = open("data/filtered_results_f.csv", "w+")
writer = csv.writer(filtered_results_f)
writer.writerow(['category', 'name', 'link', 'description'])

# The final output name
OUTPUT_NAME = "awesome_ml_filtered"

# -------------------------
# FILTERING BY PYTHON USAGE

repo_to_usage = {}

with open("../repos_languages/data/python_metadata.csv") as f:
    reader = csv.reader(f, dialect="unix")

    # headers: ['category', 'name', 'link', 'description']
    next(reader)

    for row in reader:
        repo_to_usage[row[0]] = row[1]

def allow_by_python_usage(row = None, threshold = 0.2):
    python_usage = float(repo_to_usage[row[AWL_HEADER['NAME']]])

    if python_usage < threshold * 100:
        print(f"[BLOCKED]: Reason: {python_usage} | Name:  {row[AWL_HEADER['NAME']]}")

    return python_usage >= threshold * 100
    
# -------------------------


with open(
    "data/complete_old.csv",
    "r",
    encoding="utf-8",
    newline="",
) as f:
    reader = csv.reader(f, dialect="unix")

    # headers: ['category', 'name', 'link', 'description']
    next(reader)

    for row in reader:
        if allow_by_python_usage(row):
            writer.writerow(row)

# Renaming the filtered results
os.rename('data/filtered_results_f.csv', f'data/{OUTPUT_NAME}.csv')

filtered_results_f.close()
constants_f.close()
