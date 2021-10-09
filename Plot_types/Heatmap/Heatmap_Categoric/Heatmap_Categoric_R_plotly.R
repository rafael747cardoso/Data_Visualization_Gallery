
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
x_var = "st_metratio"
x_var_name = (df_varnames %>%
                 dplyr::filter(var == x_var))$var_name
y_var = "discoverymethod"
y_var_name = (df_varnames %>%
                 dplyr::filter(var == y_var))$var_name
z_var = "pl_orbeccen"
z_var_name = (df_varnames %>%
                 dplyr::filter(var == z_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(all_of(x_var),
                            all_of(y_var),
                            all_of(z_var))
df_plot = df_plot %>% 
              tidyr::drop_na()
names(df_plot) = c("x_var", "y_var", "z_var")
my_formula = z_var ~ y_var + x_var
df_plot = xtabs(formula = my_formula,
                data = aggregate(formula = my_formula,
                                 data = df_plot,
                                 FUN = mean,
                                 drop = FALSE),
                na.action = "na.pass",
                sparse = TRUE)
x_vals = df_plot@Dimnames$x_var
y_vals = df_plot@Dimnames$y_var
df_plot = df_plot %>%
              as.matrix()

# Plot:
my_palette = c("#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04")

p = plot_ly(
        x = x_vals,
        y = y_vals,
        z = df_plot,
        type = "heatmap",
        colors = my_palette,
        colorbar = list(
            title = paste0("<b>Mean ", z_var_name, "</b>"),
            len = 1
        ),
        hovertemplate = paste0("<b>",
                               x_var_name, ": %{x}<br>",
                               y_var_name, ": %{y}<br>",
                               "Mean ", z_var_name, ": %{z:}</b><extra></extra>")
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




