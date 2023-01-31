## How and what to run ?

1. Run _collect\_test\_locations.py_ to collect stats about number of tests and its locations [test_locations .csv and .json]

2. Run _search\_for\_potential\_libs.py_ to process all test files on test_locations and discover potential libraries [test_dependencies]

3. Run _search\_for\_lib\_descriptions.py_ to search for summaries of all libs on test_dependencies. You can use it to manually filter
the ones that are related to testing.

4. Run _collect\_test\_stats.py_ to search and collect library usage on each project (the libraries to search are defined statically inside 
this file).