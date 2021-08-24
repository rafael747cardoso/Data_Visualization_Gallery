
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
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
x_var = "sy_pm"
x_var_name = (df_varnames %>%
                 dplyr::filter(var == x_var))$var_name
y_var = "st_mass"
y_var_name = (df_varnames %>%
                 dplyr::filter(var == y_var))$var_name
color_var = "disc_locale"
color_var_name = (df_varnames %>%
                     dplyr::filter(var == color_var))$var_name
size_var = "pl_orbeccen"
size_var_name = (df_varnames %>%
                     dplyr::filter(var == size_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(all_of(x_var),
                            all_of(y_var),
                            all_of(color_var),
                            all_of(size_var))

# Plot:
lvls = unique(df_plot[, color_var])
n_levels = length(lvls)
my_palette = c("#c70039", "#2a7b9b", "#eddd53")
names(my_palette) = lvls
bubble_scale = 5

p = ggplot(
        data = df_plot,
        aes(
            x = df_plot[, x_var],
            y = df_plot[, y_var],
            color = df_plot[, color_var],
            size = df_plot[, size_var],
        )
    ) +
    geom_point(
        alpha = 0.3
    ) +
    scale_size(
        range = c(0, 9),
        name = size_var_name
    ) +
    scale_color_manual(
        values = my_palette,
        name = color_var_name
    ) +
    theme(
        axis.text.x = element_text(
            size = 14,
            angle = 0,
            hjust = 0.5,
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
        legend.title = element_text(
            size = 15,
            face = "bold"
        ),
        legend.text = element_text(size = 14),
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
    xlab(x_var_name) +
    ylab(y_var_name)

p


