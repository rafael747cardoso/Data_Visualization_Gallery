
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

# Adapt the data:
df_plot = df %>%
              dplyr::group_by(eval(parse(text = x_var))) %>%
              dplyr::summarise(y_var = n()) %>%
              as.data.frame() %>%
              dplyr::rename("x_var" = "eval(parse(text = x_var))")

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))

p = plot_ly(
        data = df_plot,
        x = ~x_var,
        y = ~y_var,
        color = my_palette(3)[2],
        colors = my_palette(3)[2],
        type = "scatter",
        mode = "lines+markers",
        line = list(
            width = 5
        ),
        marker = list(
            size = 10
        ),
        hovertemplate = paste0("<b>", x_var_name, ": %{x} <br> ",
                               y_var_name, ": %{y} </b><extra></extra>")
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
        showlegend = FALSE
    )

p


