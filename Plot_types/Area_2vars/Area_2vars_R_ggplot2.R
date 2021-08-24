
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
x_var = "disc_year"
x_var_name = (df_varnames %>%
                 dplyr::filter(var == x_var))$var_name
y_var_name = "Exoplanets discovered"

# Adapt the data:
df_plot = df %>%
              dplyr::group_by(eval(parse(text = x_var))) %>%
              dplyr::summarise(y_var = n()) %>%
              as.data.frame() %>%
              dplyr::rename("x_var" = "eval(parse(text = x_var))")

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
x_axis_labels = seq(from = min(df_plot$x_var),
                    to = max(df_plot$x_var),
                    by = 4)

p = ggplot(
        data = df_plot,
        aes(
            x = x_var,
            y = y_var
        )
    ) +
    geom_line(
        show.legend = FALSE,
        color = my_palette(3)[2],
        size = 2
    ) +
    geom_area(
        fill = my_palette(3)[3]
    ) + 
    scale_x_continuous(
        labels = x_axis_labels,
        breaks = x_axis_labels
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


