
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
cat_var1 = "discoverymethod"
cat_var_name1 = (df_varnames %>%
                    dplyr::filter(var == cat_var1))$var_name
cat_var2 = "disc_locale"
cat_var_name2 = (df_varnames %>%
                    dplyr::filter(var == cat_var2))$var_name
size_var = "sy_dist"
size_var_name = (df_varnames %>%
                    dplyr::filter(var == size_var))$var_name
color_var = "dec"
color_var_name = (df_varnames %>%
                     dplyr::filter(var == color_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(all_of(cat_var1),
                            all_of(cat_var2),
                            all_of(size_var),
                            all_of(color_var))
df_plot = df_plot %>% 
              tidyr::drop_na()
df_plot = df_plot %>%
              dplyr::group_by(eval(parse(text = cat_var1)),
                              eval(parse(text = cat_var2))) %>%
              dplyr::summarise(size_var = round(mean(eval(parse(text = size_var))),
                                                digits = 2),
                               color_var = round(mean(eval(parse(text = color_var))),
                                                 digits = 2)) %>%
              as.data.frame()
names(df_plot) = c(cat_var1, cat_var2, size_var, color_var)

# Plot:
p = ggplot(
        data = df_plot,
        aes(
            area = sy_dist,
            fill = dec,
            label = disc_locale,
            subgroup = discoverymethod
        )
    ) +
    geom_treemap(
        layout = "squarified"
    ) +
    geom_treemap_text(
        colour = "white",
        place = "centre",
        size = 12,
        grow = FALSE
    ) +
    geom_treemap_subgroup_text(
        colour = "black",
        place = "top",
        size = 15,
        grow = FALSE
    ) +
    geom_treemap_subgroup_border() +
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
        title = paste0("Labels: ", cat_var_name1, ", ", cat_var_name2,
                       "\nSizes: Mean ", size_var_name),
        fill = paste0("Mean ", color_var_name)
    )

p






