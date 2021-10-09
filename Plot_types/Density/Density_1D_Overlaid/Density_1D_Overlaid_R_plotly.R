
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(plotly, lib = path_lib)

# Dataset:
df = readr::read_csv(paste0(path_data, "nasa_exoplanets.csv")) %>%
         as.data.frame()
attr(df, "spec") = NULL
df_varnames = readr::read_csv(paste0(path_data, "nasa_exoplanets_var_names.csv")) %>%
                  as.data.frame()
attr(df_varnames, "spec") = NULL

# Variables:
x_var = "sy_bmag"
x_var_name = (df_varnames %>%
                 dplyr::filter(var == x_var))$var_name
color_var = "disc_locale"
color_var_name = (df_varnames %>%
                    dplyr::filter(var == color_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(all_of(x_var),
                            all_of(color_var))
df_plot = df_plot %>% 
              tidyr::drop_na(x_var)

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
lvls = (df_plot %>%
           dplyr::select(all_of(color_var)) %>%
           unique())[, 1]
n_levels = length(lvls)

p = plot_ly()
for(l in 1:n_levels){
    lvl = lvls[l]
    df_lvl = df_plot %>%
                  dplyr::filter(eval(parse(text = color_var)) == lvl)
    dens = density(df_lvl[, x_var])
    print(my_palette(n_levels)[l])
    p = p %>%
        add_trace(
            data = df_lvl,
            x = dens$x,
            y = dens$y,
            type = "scatter",
            mode = "lines",
            color = my_palette(n_levels)[l],
            colors = my_palette(n_levels),
            name = lvl,
            text = lvl,
            hovertemplate = paste0("<b>", x_var_name, ": %{x:,}<br>",
                                   "Density: %{y:,}<br>",
                                   color_var_name, ": %{text}</b><extra></extra>")
        )
}
p = p %>%
    layout(
        xaxis = list(
            title = paste0("<b>", x_var_name, "</b>"),
            titlefont = list(
                size = 20
            ),
            tickfont = list(
                size = 18
            ),
            categoryorder = "array"
        ),
        yaxis = list(
            title = paste0("<b>Density</b>"),
            titlefont = list(
                size = 20
            ),
            tickfont = list(
                size = 18
            )
        ),
        margin = list(
            l = 10,
            r = 10,
            t = 10,
            b = 10
        ),
        hoverlabel = list(
            font = list(
                size = 18
            )
        ),
        showlegend = TRUE,
        legend = list(
            title = list(
                text = paste0("<br><b>", color_var_name, "</b>"),
                font = list(
                    size = 18
                )
            )
        )
    )

p



