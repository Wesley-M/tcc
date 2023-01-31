# It implements heuristics to narrow down possible test libraries in use
# on all repositories

# It detects imports and it checks if the potential libs are on PyPI, after that, 
# it checks if there's mentions to "tests" in the description or summary of the package.

import codecs
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

with open('data/test_locations.json') as json_file:
    test_locations = json.load(json_file)

def get_imports_from_tests(test_locations, repo_path):
    imports = set()
    
    for filepath in test_locations[repo_path]['test_files']:
        test_file = codecs.open(filepath, 'r', encoding='utf-8', errors='ignore')
        lines = test_file.readlines()
        
        for line in lines:
            if 'import' in line:
                if 'from ' in line:
                    # Spliting every space
                    module_path = line.split(' ')
                    # Removing all empty strings
                    module_path = list(filter(None, module_path))
                    # from ->package<- import ...
                    module_path = module_path[1]
                    # ->name<-.submodule.deep
                    module_name = module_path.split('.')[0].replace('\n', '')
                    # Include if its a valid identifier
                    if module_name.isidentifier():
                        imports.add(module_name)
                else:
                    try:            
                        # import pkg as a.b.c
                        module_path = line.split(' ')
                        # Removing all empty strings
                        module_path = list(filter(None, module_path))
                        # Removing import
                        module_path.pop(0)
                        # Getting only the first part of the import (import -->pkg<--.a.b.c)
                        module_name = module_path[0].split('.')[0].replace('\n', '') 
                        
                        # Include if its a valid identifier
                        if module_name.isidentifier():
                            imports.add(module_name)
                    except:
                        continue

        test_file.close()

    return imports

def is_test_dependency(package_name):
    url = "https://pypi.org/pypi/%s/json" % (package_name)
    data = json.load(urlopen(Request(url)))
    return 'test' in data["info"]["description"] or 'test' in data["info"]["summary"]

def get_valid_test_dependencies(modules):
    imports = []
    i = 1

    for module_name in modules:
        try:
            if is_test_dependency(module_name):
                print('{}. [SUCCESS] {}'.format(i, module_name))
                imports.append(module_name)
            else:
                print('{}. [NORMAL] {}'.format(i, module_name))
        except BaseException as e:
            print('{}. [ERROR] {} - {}'.format(i, module_name, str(e)))
        i += 1

    return imports


sorted_keys = sorted(list(test_locations.keys()), key=str.lower)
all_imports = set()

for repo_path in sorted_keys:
    repo_test_imports = list(get_imports_from_tests(test_locations, repo_path))
    all_imports.update(repo_test_imports)

valid = get_valid_test_dependencies(all_imports)

with open('data/test_dependencies.json', 'w', encoding='utf-8') as outfile:
    json.dump(valid, outfile)
