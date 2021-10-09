
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
x_var = "disc_year"
x_var_name = (df_varnames %>%
                 dplyr::filter(var == x_var))$var_name
y_var_name = "Exoplanets discovered"
color_var = "st_metratio"
color_var_name = (df_varnames %>%
                     dplyr::filter(var == color_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::group_by(eval(parse(text = x_var)),
                              eval(parse(text = color_var))) %>%
              dplyr::summarise(y_var = n()) %>%
              as.data.frame() %>%
              dplyr::rename("x_var" = "eval(parse(text = x_var))",
                            "color_var" = "eval(parse(text = color_var))")
df_plot$color_var = as.factor(df_plot$color_var)
df_plot = df_plot %>% 
              tidyr::drop_na("color_var")

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
n_levels = length(levels(df_plot$color_var))

p = plot_ly(
        data = df_plot,
        x = ~x_var,
        y = ~y_var,
        color = ~color_var,
        colors = my_palette(n_levels),
        text = ~color_var,
        type = "scatter",
        mode = "lines+markers",
        line = list(
            width = 5
        ),
        marker = list(
            size = 10
        ),
        hovertemplate = paste0("<b>", x_var_name, ": %{x}<br>",
                               y_var_name, ": %{y}<br>",
                               color_var_name, ": %{text}<extra></extra>")
    ) %>%
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
            title = paste0("<b>", y_var_name, "</b>"),
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


