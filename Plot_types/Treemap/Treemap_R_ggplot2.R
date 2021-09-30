
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(tidyr, lib = path_lib)
require(maditr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(ggplot2, lib = path_lib)

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
df_plot$root_lvl = "All"

# Plot:
p = ggplot(
        data = df_plot,
        aes(
            x = x_var,
            y = y_var,
            fill = Freq
        )
    ) +
    geom_tile() +
    coord_fixed(
        ratio = 1
    ) +
    scale_fill_gradientn(
        colors = my_palette(100),
        na.value = "white"
    ) +
    theme(
        axis.text.x = element_text(
            size = 14,
            angle = 0,
            hjust = 1,
            vjust = 1
        ),
        axis.text.y = element_text(size = 14),
        axis.title.x = element_text(
            size = 15,
            face = "bold"
        ),
        axis.title.y = element_text(
            size = 15,
            face = "bold"
        ),
        panel.background = element_rect(fill = "white"),
        panel.grid.major = element_line(
            size = 0.2,
            linetype = "solid",
            colour = "#eaeaea"
        ),
        panel.grid.minor = element_line(
            size = 0.1,
            linetype = "solid",
            colour = "#eaeaea"
        ),
        plot.margin = margin(
            t = 0,
            r = 5,
            b = 5, 
            l = 10,
            unit = "pt"
        )
    ) +
    labs(
        x = x_var_name,
        y = y_var_name,
        fill = paste0("Mean ", z_var_name)
    )

p






