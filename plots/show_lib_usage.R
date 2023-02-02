# It will generate a chart that shows all libs and its uses

list.of.packages <- c("tidyverse", "here", "kableExtra", "ggsci")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages) 

# Importing all the libraries
suppressMessages(library("tidyverse"))
suppressMessages(library("here"))
suppressMessages(library("kableExtra"))
suppressMessages(library("ggsci"))

source("plots/utils/utils.R")

set_base_dir("")

# Reading github metadata of each project
github_metadata <- read_csv(here(add_base_dir("analysis/stats/data/repos_stats.csv"))) %>%
  mutate(name=str_replace_all(name, " ", "_"))

libs <- read_csv(here(add_base_dir("scraping/tests/data/libs.csv")))

merged <- merge_by_column(normalize_name(github_metadata), normalize_repo_to_name(libs))

merged <- merged %>%
   transform(libs = strsplit(libs, ",")) %>%
   unnest(libs) %>%
   mutate_if(is.character, str_trim)

tot <- merged %>%
        select(name) %>%
        drop_na() %>%
        distinct %>%
        count %>%
        pull(n)

p <- merged %>% 
  select(type, libs) %>%
  group_by(libs) %>%
  mutate(lib_freq = n()) %>%
  ungroup() %>%
  group_by(libs, type) %>%
  summarise(type, lib_freq, freq = n()) %>%
  distinct %>%
  drop_na() %>%
    ggplot(aes(x = reorder(libs, lib_freq), y = freq)) + 
    geom_col(aes(fill = type), width = 0.7) +
    coord_flip() +
    scale_y_continuous(limits = c(0, 140), breaks = seq(0, 150, by = 15)) +
    labs(
        x = "",
        y = "amount of projects",
        title = "Automated test support packages",
        fill = "Project categories"
    ) +
    theme_classic() +
    theme(legend.position = c(0.57, 0.2)) +
    scale_fill_lancet() +
    theme(
      plot.title = element_text(size = 10),
      axis.text.x = element_text(size = 8),
      axis.title.x = element_text(size = 9)
    )

addSmallLegend <- function(myPlot, pointSize = 0.2, textSize = 7, spaceLegend = 0.8) {
  myPlot +
      guides(shape = guide_legend(override.aes = list(size = pointSize)),
              color = guide_legend(override.aes = list(size = pointSize)),
              fill = guide_legend(override.aes = list(size = pointSize))) +
      theme(legend.title = element_text(size = textSize), 
            legend.text  = element_text(size = textSize),
            legend.key.size = unit(spaceLegend, "lines"))
}

ggsave(
  here(add_base_dir("plots/images/libs_for_all_by_category.png")),
  addSmallLegend(p),
  width = 4.5,
  height = 5,
  dpi = 300,
  units = "in"
)