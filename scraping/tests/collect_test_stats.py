# It consolidates the information about the tests (number of test files, folders, libs being used, ...)

import codecs
import csv
import json
import re

# For more details, see: https://docs.google.com/document/d/1y8jNPS6OEmlVHbmXebPulo0Wb91jKYUl0-t70z0Zps0/edit

known_libs = [
    'nose',         # unittest
    'nose2',        # unittest2
    'testify',      # unittest
    'pytest',
    'unittest',
    'unittest2',
    'hypothesis',
    'behaviour',
    'ensure',
    'moto',
    'mongomock',
    'pytest_mock',
    'aioresponses',
    'testfixtures',
    'responses',
    'requests_mock',
    'freeze_gun',
    'fakeredis',
    'examples',
    'doctest',
    'testbook',
    'cases',
    'compare',
    'fixtures',
    'flask_testing',
    'fixture',
    'pytest_sanic',
    'pytest_kind',
    'pytest_cov',
    'pytest_timeout',
    'pytest_astropy_header',
    'pytest_cases',
    'pytests_remotedata',
    'testpath',
    'test_utils',
    'testtools',
    'xmlrunner',
    'runtests',
    'test_helpers',
    'baycomp',
    'the',
    'flaky',
    'parameterized',
    'should',
    'nose_parameterized',
    'mimesis',
    'faker'
]

# Loading all test locations
with open('data/test_locations.json') as json_file:
    test_locations = json.load(json_file)

def get_libs_from_repo(test_locations, repo_path):
    libs = set()
    libs_audit = set()
    
    def valid_import(line):
        first_word = line.strip().split(' ')[0]
        return first_word == 'import' or (first_word == 'from' and 'import' in line)
    
    def contain_lib(line, lib):
        return re.search(f' {lib}(,|\n| )?', line)
    
    for filepath in test_locations[repo_path]['test_files']:
        # Opening test file and ignoring non-utf8 characters
        test_file = codecs.open(filepath, 'r', encoding='utf-8', errors='ignore')
        
        lines = test_file.readlines()
        for line in lines:
            for lib in known_libs:
                if valid_import(line) and contain_lib(line, lib):
                    libs.add(lib)
                    libs_audit.add(line)
        
        test_file.close()

    print(repo_path)
    print(libs)

    return (libs, libs_audit)

# CSV Header
header = ['repo', 'libs', 'test_files_no', 'test_folders_no', 'test_paths', 'test_folders']

with open('data/libs.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    sorted_locations = sorted(list(test_locations.keys()), key=str.lower)

    for repo_path in sorted_locations:
        libs_repo = list(get_libs_from_repo(test_locations, repo_path)[0])
        writer.writerow([
            repo_path, 
            ','.join(libs_repo).lstrip(), 
            test_locations[repo_path]['test_files_no'],
            test_locations[repo_path]['test_folders_no']
        ])

# lib traces

sorted_locations = sorted(list(test_locations.keys()), key=str.lower)
audit = {}
for repo_path in sorted_locations:
    libs_audit = list(get_libs_from_repo(test_locations, repo_path)[1])
    audit[repo_path] = libs_audit

with open('data/lib_traces.json', 'w', encoding='utf-8') as outfile:
    json.dump(audit, outfile)

