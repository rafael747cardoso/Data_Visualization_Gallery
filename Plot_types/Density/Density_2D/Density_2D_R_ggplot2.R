
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(tidyr, lib = path_lib)
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
x_var = "sy_vmag"
x_var_name = (df_varnames %>%
                 dplyr::filter(var == x_var))$var_name
y_var = "sy_jmag"
y_var_name = (df_varnames %>%
                 dplyr::filter(var == y_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(all_of(x_var),
                            all_of(y_var))
df_plot = df_plot %>% 
              tidyr::drop_na()

# Plot:
my_palette = c("#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04")
my_palette = colorRampPalette(c("#111539", "#97A1D9"))

p = ggplot(
        data = df_plot,
        aes(
            x = eval(parse(text = x_var)),
            y = eval(parse(text = y_var))
        )
    ) +
    geom_density_2d_filled(
        na.rm = TRUE,
        contour_var = "density"
    ) +
    theme(
        axis.text.x = element_text(
            size = 14,
            angle = 0,
            hjust = 1,
            vjust = 1
        ),
        axis.text.y = element_text(
            size = 14
        ),
        axis.title.x = element_text(
            size = 15,
            face = "bold"
        ),
        axis.title.y = element_text(
            size = 15,
            face = "bold"
        ),
        panel.background = element_rect(
            fill = "white"
        ),
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
        fill = "Density"
    )

p


