
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(Hmisc, lib = path_lib)
require(reshape2, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(plotly, lib = path_lib)

# Dataset:
df = readr::read_csv(paste0(path_data, "nasa_exoplanets.csv")) %>%
         as.data.frame()
attr(df, "spec") = NULL
df_varnames = readr::read_csv(paste0(path_data, "nasa_exoplanets_var_names.csv")) %>%
                  as.data.frame()
attr(df_varnames, "spec") = NULL

num_vars = c("sy_snum", "sy_pnum", "disc_year", "pl_orbeccen", "st_teff", "st_mass", "sy_pm",
             "sy_dist", "sy_gaiamag")
num_vars_names = (df_varnames %>%
                     dplyr::filter(var %in% num_vars))$var_name

# Adapt the data:
df_plot = df[, num_vars]
names(df_plot) = num_vars_names
df_plot = df_plot %>% 
              tidyr::drop_na()
df_plot = (df_plot %>%
              as.matrix() %>%
              rcorr(type = "pearson"))$r
df_plot = melt(data = df_plot,
               value.name = "Vars_corr")

# Plot:
my_palette = c("#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04")

p = plot_ly(
    data = df_plot,
    x = ~Var1,
    y = ~Var2,
    z = ~Vars_corr,
    type = "heatmap",
    colors = my_palette,
    colorbar = list(
        title = "<b>Pearson correlation</b>",
        len = 1
    ),
    hovertemplate = paste0("<b>",
                           "%{x}<br>",
                           "%{y}<br>",
                           "Correlation: %{z:}</b><extra></extra>")
) %>%
    layout(
        height = 900,
        width = 1200,
        xaxis = list(
            title = "",
            tickfont = list(size = 18),
            categoryorder = "array"
        ),
        yaxis = list(
            title = "",
            tickfont = list(size = 18)
        ),
        margin = list(
            l = 10,
            r = 10,
            t = 10,
            b = 10
        ),
        hoverlabel = list(font = list(size = 18))
    )

p




