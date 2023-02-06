list.of.packages <- c("tidyverse", "here", "kableExtra")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages) 

# Importing all the libraries
suppressMessages(library("tidyverse"))
suppressMessages(library("here"))
suppressMessages(library("kableExtra"))
suppressMessages(library("forcats"))

source("plots/utils/utils.R")

set_base_dir("")

to_sonar_key <- function(name) {
  return(str_replace_all(name, c(" " = "_", "\\?" = "_", "\\(" = "_", "\\)" = "_", "’" = "_")))
}

# Importing files

issues <- read_csv(here(add_base_dir("analysis/issues/data/issues.csv")))

github_metadata <- read_csv(here(add_base_dir("analysis/stats/data/repos_stats.csv"))) %>%
  mutate(name=to_sonar_key(name))

qube_stats <- read_csv(here(add_base_dir("analysis/stats/data/repo_qube_stats.csv"))) %>%
  mutate(name=to_sonar_key(name))

libs <- read_csv(here(add_base_dir("scraping/tests/data/libs.csv")))
libs <- normalize_repo_to_name(libs) %>%
  mutate(name=to_sonar_key(name))

# Mutating and merging

libs_stats <- merge(libs, qube_stats, by = "name") %>%
  group_by(type) %>%
  mutate(
    repo_type_count_with_tests = sum(!is.na(libs)),
    repo_type_count_without_tests = sum(is.na(libs))
  ) %>%
  ungroup()

issues <- issues %>% rename("name" = project)

merged_issues <- merge(x = issues, y = github_metadata, by = "name") %>%
  rename(issue_type = "type.x", repo_type = "type.y")

bugs <- merge(merged_issues, libs_stats, by = "name") %>%
    filter(issue_type == "BUG")

bugs <- bugs %>%
    mutate(normalized_bug = 1 / ncloc)

# ----

diff <- function(m, n) {
    r <- ifelse(!is.finite( ((m - n) / n) ), result <- "Infinite**", result <- paste0(round(((m - n) / n) * 100, 2), "%"))
    return(r)
}

bugs %>%
  group_by(repo_type, severity) %>%
  summarise(
    difference = diff(
      # Mean of normalized bugs by category count [with tests]
      sum(normalized_bug[!is.na(libs)]) / repo_type_count_with_tests,
      # Mean of normalized bugs by category count [without tests]
      sum(normalized_bug[is.na(libs)]) / repo_type_count_without_tests
    )
  ) %>%
  distinct() %>%
  pivot_wider(names_from = severity, values_from = difference, values_fill = list(difference = "Undefined*")) %>%
  kbl(format = "latex") %>%
    footnote(symbol = c("There is no combination of category and bug severity present in the data.",
                        "This combination does not exist in the projects without tests.")
    ) %>%
    kable_styling(full_width = F, bootstrap_options = c("condensed")) %>%
    kable_classic() %>%
    save_kable(here(add_base_dir("plots/images/bugs_sonarqube.tex")), density = 300)