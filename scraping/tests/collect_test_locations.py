"""
It implements a simple heuristic to identify test files / folders (checking if there is "test" in its name). 
"""

import csv
import glob
import json


# It gets all the filepaths from python files that have 'test' in their name
def get_all_test_files(dir):
    filepaths = []

    for filepath in glob.iglob('{}/**/*.py'.format(dir), recursive=True):
        filename = filepath.split('/')[-1].lower()
        if 'test' in filename:
            filepaths.append(filepath)
    
    return filepaths

# It gets all the filepaths from folders that have 'test' in their name
def get_all_test_folders(dir):
    filepaths = []

    for filepath in glob.iglob('{}/**/'.format(dir), recursive=True):
        # Getting the last folder name
        filename = filepath.split('/')[-2].lower()
        if 'test' in filename:
            filepaths.append(filepath)
    
    return filepaths

# It gets all repo file paths
def get_all_immediate_subdirectories(dir):
    filepaths = []

    for filepath in glob.iglob('{}/*/'.format(dir), recursive=True):
        filepaths.append(filepath)
    
    return filepaths

all_repos_filepaths = get_all_immediate_subdirectories('../../repos')

#--- COLLECTS ALL FILE AND FOLDER PATHS

json_tests = {}
csv_tests = []

for repo_filepath in all_repos_filepaths:
    test_files = get_all_test_files(repo_filepath)
    test_folders = get_all_test_folders(repo_filepath)
    test_files_no = len(test_files)
    test_folders_no = len(test_folders)

    json_tests[repo_filepath] = {
        'test_files': test_files,
        'test_folders': test_folders,
        'test_files_no': test_files_no,
        'test_folders_no': test_folders_no
    }

    csv_tests.append({
        'repo': repo_filepath,
        'test_files_no': test_files_no,
        'test_folders_no': test_folders_no
    })

with open('data/test_locations.json', 'w', encoding='utf-8') as outfile:
    json.dump(json_tests, outfile)

with open('data/test_locations.csv', 'w', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['repo', 'test_files_no', 'test_folders_no'])
    writer.writeheader()
    writer.writerows(csv_tests)
