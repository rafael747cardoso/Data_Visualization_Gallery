
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

# Plot:
my_palette = list(
    list(0, "#000000"),
    list(0.25, "#E008F8"),
    list(0.5, "#F81D08"),
    list(0.75, "#F88A08"),
    list(1, "#F7FE04")
)
n_binsxy = 150

p = plot_ly(
        data = df_plot,
        x = ~eval(parse(text = x_var)),
        y = ~eval(parse(text = y_var)),
        type = "histogram2d",
        histfunc = "bin",
        histnorm = "",
        nbinsx = n_binsxy,
        nbinsy = n_binsxy,
        xbins = list(
            start = 0,
            end = 20
        ),
        ybins = list(
            start = 0,
            end = 20
        ),
        colorscale = my_palette,
        colorbar = list(
            title = "<b>Counts</b>"
        ),
        hovertemplate = paste0("<b>",
                               x_var_name, ": %{x:,}<br>",
                               y_var_name, ": %{y:,}<br>",
                               "Counts: %{z:}</b><extra></extra>")
    ) %>%
    layout(
        height = 800,
        width = 800,
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
        )
    )

p


