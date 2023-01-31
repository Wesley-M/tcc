## How and what to run ?

1. Run _raw\_scrape.py_ to collect the original repo list

2. Run _search\_urls\_outside\_github.py_ to isolate which projects have links pointing outside github [unknown_repos.csv]

3. Run _collect\_github\_urls.py_ to search for the potential project links inside github [awesome_ml_plus_unknown_urls.csv] 

4. Run _filter\_out\_repos.py_ to more fine grained filtering of repos. [awesome_ml_filtered.csv]

## Observations

Just to clarify it, "data/awesome\_ml\_mv.csv" is the manually verified list after careful evaluation.