# This script will generate a table that shows the test adoption for all categories of projects

list.of.packages <- c("tidyverse", "here", "kableExtra", "janitor")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages) 

# Importing all the libraries
suppressMessages(library("tidyverse"))
suppressMessages(library("here"))
suppressMessages(library("kableExtra"))
suppressMessages(library("janitor"))

source("plots/utils/utils.R")

set_base_dir("")

# Reading github metadata of each project
github_metadata <- read_csv(here(add_base_dir("analysis/stats/data/repos_stats.csv"))) %>%
  mutate(name=str_replace_all(name, " ", "_"))

# Reading repo libraries information
repo_libraries <- read_csv(here(add_base_dir("scraping/tests/data/libs.csv")))

# Reading test location information about the repos
test_locations <- read_csv(here(add_base_dir("scraping/tests/data/test_locations.csv")))

View(repo_libraries)

# Adding type column to the the repo libraries dataframe
merged <- merge_by_column(normalize_repo_to_name(repo_libraries), normalize_name(github_metadata)) %>%
    select(name, type, libs) %>%
    distinct(name, type, .keep_all = TRUE)

merged <- merge_by_column(merged, normalize_repo_to_name(test_locations)) %>%
    select(name, type, libs, test_files_no)

# ADOPTION BY TEST LIB USAGE

# Consolidating the data into a table
adoption_by_imports <- merged %>%
  mutate(has_imports = ifelse(is.na(libs), 0, 1)) %>%
  group_by(type) %>%
  summarise(
    adoption_abs = sum(has_imports == 1),
    neglect_abs = sum(has_imports == 0),
    total = n(),
    adoption_freq = paste(round(adoption_abs * 100 / total, 2), "%"),
    neglect_freq = paste(round(neglect_abs * 100 / total, 2), "%")
  ) %>%
  select(type, adoption_abs, adoption_freq, total) %>%
  mutate(freq = paste(adoption_abs, "/", total)) %>%
  arrange(desc(adoption_abs / total)) %>%
  select(type, freq, adoption_freq)

# Totals
totals <- merged %>%
  mutate(has_imports = ifelse(is.na(libs), 0, 1)) %>%
  summarise(
    type = "Total",
    freq = paste(sum(has_imports == 1), "/", n()),
    adoption_freq = paste(round(sum(has_imports == 1) * 100 / n(), 2), "%"),
  )

adoption_by_imports <- rbind(adoption_by_imports, totals)

# Creating the png table
adoption_by_imports %>%
  rename("Categoria do projeto" = type, "Proporção" = freq, "Adoção (%)" = adoption_freq) %>%
  kbl() %>%
  kable_styling(full_width = F) %>%
  save_kable(here(add_base_dir("plots/images/adoption_table_by_imports.png")))