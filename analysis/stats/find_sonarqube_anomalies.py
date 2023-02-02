"""
It checks if there is anything strange in the sonarqube stats that were reported
"""

import csv

repos = []
result = []

# How much empty fields there is need to be in a line to consider the evaluation faulty
threshold = 3

anomalies = []

# Reading repos
with open(
    "./data/repo_qube_stats.csv",
    "r",
    encoding="utf-8",
    newline="",
) as f:
    reader = csv.reader(f, dialect="unix")

    next(reader)

    count = 0
    for row in reader:
        for cell in row:
            if not cell:
                count += 1
        if count >= threshold:
            anomalies.append(row[0])
        count = 0

print(anomalies)

with open('./data/anomalies.csv', 'w', newline='\n') as file:
    file.write('anomalies\n')
    for a in anomalies:
        file.write(a)
        file.write('\n')
