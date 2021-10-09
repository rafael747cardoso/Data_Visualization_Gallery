
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

# Adapt the data:
x_vals = df[, x_var]

# Plot:
p = plot_ly(
        x = x_vals,
        type = "histogram",
        histfunc = "count",
        histnorm = "",
        nbinsx = 100,
        color = "#813DDA",
        colors = "#813DDA",
        opacity = 0.9,
        hovertemplate = paste0("<b>Counts: %{y:,}<br>",
                               x_var_name, ": %{x:,}</b><extra></extra>")
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
            title = paste0("<b>Counts</b>"),
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





