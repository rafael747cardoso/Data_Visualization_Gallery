
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(tidyr, lib = path_lib)
require(maditr, lib = path_lib)
require(readr, lib = path_lib)
require(ggplot2, lib = path_lib)
require(treemapify, lib = path_lib)

# Dataset:
df = readr::read_csv(paste0(path_data, "nasa_exoplanets.csv")) %>%
         as.data.frame()
attr(df, "spec") = NULL
df_varnames = readr::read_csv(paste0(path_data, "nasa_exoplanets_var_names.csv")) %>%
                  as.data.frame()
attr(df_varnames, "spec") = NULL

# Variables:
cat_var = "discoverymethod"
cat_var_name = (df_varnames %>%
                   dplyr::filter(var == cat_var))$var_name
size_var = "sy_dist"
size_var_name = (df_varnames %>%
                    dplyr::filter(var == size_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(all_of(cat_var),
                            all_of(size_var))
df_plot = df_plot %>% 
              tidyr::drop_na()
df_plot = df_plot %>%
              dplyr::group_by(eval(parse(text = cat_var))) %>%
              dplyr::summarise(size_var = round(mean(eval(parse(text = size_var))),
                                                digits = 2)) %>%
              as.data.frame()
names(df_plot) = c(cat_var, size_var)
df_plot$groups = 1:nrow(df_plot)
df_plot$root_lvl = "All"

# Plot:
p = ggplot(
        data = df_plot,
        aes(
            area = groups,
            fill = sy_dist,
            label = discoverymethod
        )
    ) +
    geom_treemap() +
    geom_treemap_text(
        colour = "white",
        place = "centre",
        size = 15,
        grow = TRUE
    ) +
    scale_fill_viridis_c() +
    
    theme(
        panel.background = element_rect(fill = "white"),
        plot.margin = margin(
            t = 10,
            r = 5,
            b = 5, 
            l = 10,
            unit = "pt"
        )
    ) +
    labs(
        title = paste0("Labels: ", cat_var_name, "\nSizes: Mean ", size_var_name),
        fill = paste0("Mean ", size_var_name)
    )

p






