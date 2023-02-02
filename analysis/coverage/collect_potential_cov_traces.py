"""
It collects potential traces of coverage information in the repositories README.md
"""

import csv
import json
import re
import sys

csv.field_size_limit(sys.maxsize)

# Constants
constants_f = open('../../config/constants.json')
constants = json.load(constants_f)

HEADER = constants["AWESOME_HEADER_ENUM"]

README_API = "https://raw.githubusercontent.com/{}/{}/{}/README.{}"

traces = {}

with open(
    "data/readmes_with_cov.csv",
    "r",
    encoding="utf-8",
    newline="",
) as f:
    reader = csv.reader(f, dialect="unix")

    # headers: ['repo', 'content']
    next(reader)
        
    i = 0
    for row in reader:
        print('---')
        print(f'Requesting README from {row[0]}.')
        
        readme = row[1]
        
        if 'cov' in readme.lower():
            cov_traces = re.findall(r"(^.*?%s.*?$)" % 'cov', readme, flags=re.MULTILINE | re.IGNORECASE) 
            traces[row[0]] = cov_traces
        else:
            print(f'[ERROR]')

        i += 1

with open('data/cov_traces.json', 'w', encoding='utf-8') as outfile:
    json.dump(traces, outfile)
