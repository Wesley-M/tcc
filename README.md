## Understanding the testing culture of machine learning projects on Github

The current repository serves as a storage for all scripts used for the paper purposes.

Before we dive in deeper in the repo structure, make sure to have a Github API token setup.
Several of the scripts depend on it.

    Create a .env file with your token on the root dir, with the content:
        PERSONAL_TOKEN=YOUR_TOKEN

### Where to start ?

First, you should run the "setup.py" script. It will clone all the machine learning
repos on your machine for further analysis.

### Repository folder structure

The repository is structured as follows:

1. The scraping folder is composed of repo_list and tests. These contain the scripts
for scraping the "Awesome machine learning repository" and all the test statistics. Each
folder has a README.md, where you can find the instructions and usage of the scripts;

2. The plots folder has all R scripts being used to plot the paper tables and figures;

3. Analysis folder is composed of coverage, issues, languages and stats sub-folders. Each
one of them have their respective scripts and instructions. 

### To reproduce the research you could: 

#### Work in progress