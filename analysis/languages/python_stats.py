import json

"""
It reads from languages_metadata and extracts python stats
"""

metadata_file = open('data/languages_metadata.json')

metadata = json.load(metadata_file)

with open('data/python_metadata.csv', 'w') as f:
    f.write("repo,py_percentage\n")
    i = 0
    for repo in metadata.keys():
        total = 0
        python = 0

        for language in metadata[repo]:
            bytes = metadata[repo][language]
            total += bytes

            if language == 'Python':
                python = bytes

        if total == 0 and python == 0:
            python = 1
            total = 1
        
        print(f"[{i+1}]: {repo} | python: {python}, total: {total}, prop: {round(python * 100 / total, 2)}")
        i += 1

        f.write("%s,%s\n" % (repo, round(python * 100 / total, 2)))

metadata_file.close()
