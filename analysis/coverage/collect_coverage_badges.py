import csv
import json
import re

# It tries to get the links for the coverage badges in the repos README.md

services = [
    'coveralls',
    'codecov',
    'codeclimate',
    'cov'
]

def get_badge_urls(text):
    result = set()
    matched = re.findall(r'(?:http\:|https\:)\/\/.*', text)
    
    for match in matched:
        for service in services:
            if service in match:
                result.add(match)
                break
    
    return list(result)

def get_badge_images(text):
    result = set()
    matched = re.findall(r'(?:http\:|https\:)\/\/.*\.(?:png|jpg|svg)', text)
    
    for match in matched:
        for service in services:
            if service in match:
                result.add(match)
                break
    
    return list(result)



f = open('data/cov_traces.json')
traces = json.load(f)

badges = []

for repo in traces:
    links = []
    images = []
    
    for line in traces[repo]:
        links.extend(get_badge_urls(line))
        images.extend(get_badge_images(line))
    
    if not (links == [] and images == []):
        badges.append({
            'name': repo,
            'links': links,
            'images': images
        })

with open('data/badges.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'links', 'images'])
    writer.writeheader()
    writer.writerows(badges)

f.close()
