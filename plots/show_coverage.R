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

# Reading github metadata of each project
github_metadata <- read_csv(here(add_base_dir("analysis/stats/data/repos_stats.csv"))) %>%
  mutate(name=str_replace_all(name, " ", "_"))

cov <- read_csv(here(add_base_dir("analysis/coverage/data/coverage_mv.csv")))

merged <- merge_by_column(normalize_name(github_metadata), cov) %>% filter(!is.na(coverage))

merged <- merged %>%
    mutate(tracking_tool = ifelse(grepl("codecov", images, fixed = TRUE),
        "codecov",
        ifelse(grepl("coveralls", images, fixed = TRUE),
            "coveralls",
            ifelse(grepl("codeclimate", images, fixed = TRUE),
                "codeclimate",
                "self-hosted"
            )
        )
    ))

print(nrow(github_metadata))

merged %>%
    select(tracking_tool) %>%
    group_by(tracking_tool) %>%
    rename("Coverage tracking tool" = tracking_tool) %>%
    summarise("# of projects that adopt the tool" = n(), "%" = paste(round(n() / nrow(github_metadata) * 100, 2), "%")) %>%
    arrange(desc(`# of projects that adopt the tool`)) %>%
    kbl() %>%
    kable_styling(full_width = F) %>%
    save_kable(here(add_base_dir("plots/images/coverage_tracking_tool.png")))

total_projects <- github_metadata %>%
    group_by(type) %>%
    summarise(tot = n())

old_cov_by_type <- merged %>%
        group_by(type) %>%
        summarise(n = n(), mean = mean(coverage)) %>%
        arrange(desc(mean))

cov_by_type <- merge(total_projects, old_cov_by_type, by = "type") %>%
    arrange(desc(mean)) %>%
    mutate(
        proportion_abs = paste0(n, "/", tot),
        proportion = paste(round(n / tot * 100, 2), "%"), 
        mean = paste(round(mean, 2), "%")
    ) %>%
    select(type, proportion_abs, proportion, mean) %>%
    rename(
        "# of projects that publish coverage" = proportion_abs,
        "%" = proportion,
        "Mean coverage (%)" = mean,
        "Category" = type
    )

totals <- merge(total_projects, old_cov_by_type, by = "type") %>%
    ungroup() %>%
    summarise(
        "# of projects that publish coverage" = paste0(nrow(cov), "/", nrow(github_metadata)),
        "%" = paste(round(nrow(cov) / nrow(github_metadata) * 100, 2), "%"),
        "Mean coverage (%)" = paste(round(mean(cov$coverage), 2), "%"),
        "Category" = "Overall"
    )

rbind(cov_by_type, totals) %>%
    kbl() %>%
    kable_styling(full_width = F) %>%
    save_kable(here(add_base_dir("plots/images/cov_by_type.png")))
