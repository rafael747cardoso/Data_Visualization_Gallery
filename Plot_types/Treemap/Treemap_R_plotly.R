
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
cat_var = "discoverymethod"
cat_var_name = (df_varnames %>%
                   dplyr::filter(var == cat_var))$var_name
size_var = "sy_dist"
size_var_name = (df_varnames %>%
                    dplyr::filter(var == size_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(all_of(cat_var),
                            all_of(size_var))
df_plot = df_plot %>% 
              tidyr::drop_na()
df_plot = df_plot %>%
              dplyr::group_by(eval(parse(text = cat_var))) %>%
              dplyr::summarise(size_var = round(mean(eval(parse(text = size_var))),
                                                digits = 2)) %>%
              as.data.frame()
names(df_plot) = c(cat_var, size_var)
df_plot$root_lvl = "All"

# Plot:
p = plot_ly(
    data = df_plot,
    parents = ~root_lvl,
    labels = ~eval(parse(text = cat_var)),
    values = ~eval(parse(text = size_var)),
    textinfo = "parent+label+value",
    type = "treemap",
    marker = list(
        colorscale = "Viridis"
    )
) %>%
    layout(
        title = paste0("Labels: ", cat_var_name, "<br>Sizes: Mean ", size_var_name),
        margin = list(
            l = 10,
            r = 10,
            t = 60,
            b = 10
        ),
        hoverlabel = list(
            font = list(
                size = 18
            )
        )
    )

p


