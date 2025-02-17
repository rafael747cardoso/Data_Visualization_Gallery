
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
cat_var1 = "st_metratio"
cat_var_name1 = (df_varnames %>%
                    dplyr::filter(var == cat_var1))$var_name
cat_var2 = "disc_locale"
cat_var_name2 = (df_varnames %>%
                     dplyr::filter(var == cat_var2))$var_name
num_var = "sy_dist"
num_var_name = (df_varnames %>%
                    dplyr::filter(var == num_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(cat_var1,
                            cat_var2,
                            num_var)
df_plot[which(is.na(df_plot[, cat_var1])), cat_var1] = "NA"
df_plot[which(is.na(df_plot[, cat_var2])), cat_var2] = "NA"
df_plot = df_plot[which(!is.na(df_plot[, num_var])), ]

# Levels order:
sorted_levels1 = sort(unique(df_plot[, cat_var1]))
df_plot[, cat_var1] = factor(x = df_plot[, cat_var1],
                             levels = sorted_levels1)
sorted_levels2 = sort(unique(df_plot[, cat_var2]))
df_plot[, cat_var2] = factor(x = df_plot[, cat_var2],
                             levels = sorted_levels2)

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
n_levels2 = length(unique(df_plot[, cat_var2]))
p = plot_ly(
        data = df_plot,
        type = "violin",
        x = ~eval(parse(text = cat_var1)),
        y = ~eval(parse(text = num_var)),
        color = ~eval(parse(text = cat_var2)),
        colors = my_palette(n_levels2),
        spanmode = "hard",
        alpha = 1,
        box = list(
            visible = FALSE
        ),
        meanline = list(
            visible = FALSE
        ),
        points = FALSE,
        scalemode = "width"  ### this doesn't work (R plotly bug?)
    ) %>%
    layout(
        xaxis = list(
            title = paste0("<b>", cat_var_name1, "</b>"),
            titlefont = list(
                size = 20
            ),
            tickfont = list(
                size = 18
            ),
            categoryorder = "array"
        ),
        yaxis = list(
            title = paste0("<b>", num_var_name, "</b>"),
            titlefont = list(
                size = 20
            ),
            tickfont = list(
                size = 18
            ),
            type = "log"
        ),
        margin = list(
            l = 10,
            r = 10,
            t = 10,
            b = 10
        ),
        legend = list(
            title = list(
                text = paste0("<br><b>", cat_var_name2, "</b>"),
                font = list(
                    size = 18
                )
            )
        ),
        hoverlabel = list(
            font = list(
                size = 16
            )
        ),
        showlegend = TRUE,
        violinmode = "group"
    )

p


