"""
Search the description of all the potential test libraries
"""

import json
from urllib.request import Request, urlopen

with open('data/test_dependencies.json') as json_file:
    dependencies = json.load(json_file)

def get_metadata(package_name):
    url = "https://pypi.org/pypi/%s/json" % (package_name)
    data = json.load(urlopen(Request(url)))
    return data["info"]

metadata = {}
i = 1
for dep in dependencies:
    print(f"[{round(i*100 / len(dependencies), 2)}%] Requesting metadata from {dep}")
    
    m = get_metadata(dep)
    metadata[dep] = {
        'summary': m['summary']
    }

    i+=1

with open('data/test_dependencies_metadata.json', 'w', encoding='utf-8') as outfile:
    json.dump(metadata, outfile)
