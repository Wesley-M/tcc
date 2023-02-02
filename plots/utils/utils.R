suppressMessages(library("tidyverse"))

base_dir <- "tcc_code"

add_base_dir <- function(path) {
  if (base_dir != "") {
    return(paste(base_dir, path, sep="/"))
  }
  return(path)
}

set_base_dir <- function(new_base) {
  base_dir <<- new_base
}

# Merging rows (left join) by a column (case sensitive)
merge_by_column <- function(x, y, column = "name") {
  x <- as_tibble(x)
  y <- as_tibble(y)

  x[column] <- tolower(x[[column]])
  y[column] <- tolower(y[[column]])

  df <- merge(x = x, y = y, by = column, all.x = TRUE)

  return(df)
}

# Normalizing the repo path to its name
#  - Its used when a dataframe has a "repo" column with a path, but we just need the name of the repo. 
normalize_repo_to_name <- function(df) {
    normalized <- df %>%
      rename(name = repo)

    normalized <- normalize_name(normalized) %>%
      mutate(name = str_replace(name, "/", ""))
    
    return(normalized)
}

normalize_name <- function(df) {
    normalized <- df %>%
        mutate(name = str_replace(name, "../../repos/", "")) %>%
        mutate(name = sapply(str_split(name, "/"), function(x) x[1]))
      
    return(normalized)
}