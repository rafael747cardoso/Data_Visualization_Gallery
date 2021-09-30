
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
cat_var1 = "discoverymethod"
cat_var_name1 = (df_varnames %>%
                    dplyr::filter(var == cat_var1))$var_name
cat_var2 = "disc_locale"
cat_var_name2 = (df_varnames %>%
                    dplyr::filter(var == cat_var2))$var_name
size_var = "sy_dist"
size_var_name = (df_varnames %>%
                    dplyr::filter(var == size_var))$var_name
color_var = "dec"
color_var_name = (df_varnames %>%
                     dplyr::filter(var == color_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(all_of(cat_var1),
                            all_of(cat_var2),
                            all_of(size_var),
                            all_of(color_var))
df_plot = df_plot %>% 
              tidyr::drop_na()

# df_plot = df_plot %>%
#               dplyr::group_by(eval(parse(text = cat_var1)),
#                               eval(parse(text = cat_var2))) %>%
#               dplyr::summarise(size_var = mean(eval(parse(text = size_var))),
#                                color_var = mean(eval(parse(text = color_var)))) %>%
#               as.data.frame() %>%
# names(df_plot) = c(cat_var1, cat_var2, size_var, color_var)


require(treemap)

treemap(
    dtf = df_plot,
    index = c(cat_var1, cat_var2),
    vSize = size_var,
    vColor = color_var,
    title = "title here with the variables used",
    palette = "RdBu",
    align.labels = list(
        c("left", "top"),
        c("center", "center")
    )
)


# df_root = data.frame(cat_var1 = "",
#                      cat_var2 = "All",
#                      size_var = 1000,
#                      color_var = -90,
#                      stringsAsFactors = FALSE)
# names(df_root) = c(cat_var1, cat_var2, size_var, color_var)
# df_plot = rbind(
#     df_root,
#     df_plot
# )


# Plot:
p = plot_ly(
    # data = df_plot,
    # parents = ~eval(parse(text = cat_var1)),
    # labels = ~eval(parse(text = cat_var2)),
    # values = ~eval(parse(text = size_var)),
    
    parents = c(  "",   "Eve",  "Eve", "Seth", "Seth",  "Eve",  "Eve",  "Awan",   "Eve"),
    labels =  c("Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"),
    values =  c(   15,     21,     12,     10,      2,      6,      6,       4,       4),
    
    # parents = df1$parents,
    # labels = df1$labels,
    # ids = df1$ids,

    type = "treemap",
    marker = list(
        colorscale = "Viridis"
    )
) %>%
    layout(
        margin = list(
            l = 10,
            r = 10,
            t = 30,
            b = 10
        ),
        hoverlabel = list(
            font = list(
                size = 18
            )
        )
    )

p




