
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
         as.data.frame() %>%
attr(df, "spec") = NULL
df_varnames = readr::read_csv(paste0(path_data, "nasa_exoplanets_var_names.csv")) %>%
                  as.data.frame()
attr(df_varnames, "spec") = NULL

# Variables:
cat_var = "discoverymethod"
cat_var_name = (df_varnames %>%
                    dplyr::filter(var == cat_var))$var_name
num_var = "sy_dist"
num_var_name = (df_varnames %>%
                    dplyr::filter(var == num_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(cat_var,
                            num_var)

# Deal with NA:
df_plot[which(is.na(df_plot[, cat_var])), cat_var] = "NA"

# Levels order:
sorted_levels = sort(unique(df_plot[, cat_var]))
df_plot[, cat_var] = factor(x = df_plot[, cat_var],
                            levels = sorted_levels)

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
n_levels = length(unique(df_plot[, cat_var]))
p = plot_ly(
    data = df_plot,
    type = "box",
    y = ~eval(parse(text = num_var)),
    color = ~eval(parse(text = cat_var)),
    colors = my_palette(n_levels)
    # hovertemplate = paste0("<b>Frequency: %{y:,}<br>", 
    #                        cat_var_name2, ": %{x}<br>", 
    #                        cat_var_name1, ": %{text}</b><extra></extra>")
) %>%
    layout(
        xaxis = list(
            title = paste0("<b>", cat_var_name, "</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18),
            categoryorder = "array"
        ),
        yaxis = list(
            title = paste0("<b>", num_var_name, "</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18),
            type = "linear"
        ),
        margin = list(
            l = 50,
            r = 10,
            t = 10,
            b = 10
        ),
        hoverlabel = list(font = list(size = 16)),
        showlegend = FALSE
    )

p










