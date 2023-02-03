list.of.packages <- c("tidyverse", "here", "kableExtra")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages) 

# Importing all the libraries
suppressMessages(library("tidyverse"))
suppressMessages(library("here"))
suppressMessages(library("kableExtra"))

source("plots/utils/utils.R")

set_base_dir("")

options(scipen=999)

# Cognitive & Ciclomatic Complexity
# Vulnerabilities
# Technical Debt
# Duplications

# Reading github metadata of each project
github_metadata <- read_csv(here(add_base_dir("analysis/stats/data/repos_stats.csv"))) %>%
  mutate(name=str_replace_all(name, " ", "_"))

libs <- read_csv(here(add_base_dir("scraping/tests/data/libs.csv")))

merged <- merge_by_column(normalize_name(github_metadata), normalize_repo_to_name(libs))

qube_stats <- read_csv(here(add_base_dir("analysis/stats/data/repo_qube_stats.csv"))) %>%
  mutate(name=str_replace_all(name, " ", "_"))

temp_without_tests <- merged %>%
  filter(is.na(libs))

temp_with_tests <- merged %>%
  filter(!is.na(libs))

# Databases for the projects with and without tests
with_tests <- merge_by_column(normalize_name(temp_with_tests), qube_stats)
without_tests <- merge_by_column(normalize_name(temp_without_tests), qube_stats)

header1 <- "With automated tests (N = 192)"
header2 <- "Without automated tests (N = 101)"

with_tests <- with_tests %>%
  mutate(
    bugs_normalized_by_loc = as.numeric(bugs / ncloc),
    smells_normalized_by_loc = as.numeric(code_smells / ncloc),
    technical_debt_by_loc = as.numeric(sqale_index / ncloc),
    reliability_remediation_effort_by_loc = as.numeric(reliability_remediation_effort / ncloc),
    vulnerabilities_by_loc = as.numeric(vulnerabilities / ncloc)
  )

without_tests <- without_tests %>%
  mutate(
    bugs_normalized_by_loc = as.numeric(bugs / ncloc),
    smells_normalized_by_loc = as.numeric(code_smells / ncloc),
    technical_debt_by_loc = as.numeric(sqale_index / ncloc),
    reliability_remediation_effort_by_loc = as.numeric(reliability_remediation_effort / ncloc),
    vulnerabilities_by_loc = as.numeric(vulnerabilities / ncloc)
  )

stats <- function(tests_df, column, label = "Complexidade") {
  standardize <- function(v) {
    return(v)
  }
  
  return(
    tribble(
      ~ lab,
      ~ stat,
      ~ result,
      label,
      "Min",
      standardize(min(tests_df[[column]], na.rm = TRUE)),
      label,
      "Mean",
      standardize(mean(tests_df[[column]], na.rm = TRUE)),
      label,
      "Median",
      standardize(median(tests_df[[column]], na.rm = TRUE)),
      label,
      "Max",
      standardize(max(tests_df[[column]], na.rm = TRUE))
    )
  )
}

concat_rows <- function(column, label, df1 = with_tests, df_lab = header1, df2 = without_tests, df2_lab = header2) {
  diff <- function(m, n) {
    r <-
      ifelse(!is.finite(((m - n) / n)),
             result <-
               "Undefined*",
             result <- paste0(round(((
               m - n
             ) / n) * 100, 2), "%"))
    return(r)
  }
  
  tab <- inner_join(
    stats(df1, column, label) %>% rename(!!df_lab := "result"),
    stats(df2, column, label) %>% rename(!!df2_lab := "result"),
    by = c("stat", "lab")
  )
  
  tab <- tab %>%
    mutate("Percentual Increase" = diff(tab[[df_lab]], tab[[df2_lab]]))
  
  return(tab)
}
  
tab <- bind_rows(
  concat_rows(
    "ncloc",
    "Lines of code (LOC)"
  ),
  concat_rows(
    "cognitive_complexity",
    "Cognitive Complexity (CC)"
  ),
  concat_rows(
    "duplicated_lines_density",
    "Duplicated lines (%)"
  ),
  concat_rows(
    "bugs_normalized_by_loc",
    "Bugs (normalized by LOC)"
  ),
  concat_rows(
    "reliability_remediation_effort_by_loc",
    "Reliability Remediation Effort in minutes (normalized by LOC)"
  ),
  concat_rows(
    "smells_normalized_by_loc",
    "Smells (normalized by LOC)"
  ),
  concat_rows(
    "technical_debt_by_loc",
    "Technical Debt in minutes (normalized by LOC)"
  ),
  concat_rows(
    "vulnerabilities_by_loc",
    "Vulnerabilities (normalized by LOC)"
  )
)

tab %>%
    select(stat, !!header2, !!header1, "Percentual Increase") %>%
    rename("Characteristic" = stat) %>%
    kbl(format = "latex") %>%
    footnote(symbol = c("The difference can not be determined, given one of the values is 0.")) %>%
    kable_styling(full_width = F, bootstrap_options = c("condensed")) %>%
    kable_classic() %>%
    row_spec(0, bold = T) %>%
    pack_rows(index = table(factor(tab$lab, levels=unique(tab$lab)))) %>%
    save_kable(here(add_base_dir("plots/images/descriptive_table_sonarqube.tex")), density = 300)
