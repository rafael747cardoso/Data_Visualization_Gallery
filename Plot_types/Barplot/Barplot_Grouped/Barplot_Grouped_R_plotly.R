
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
cat_var1 = "pl_letter"
cat_var2 = "discoverymethod"
cat_var_name1 = (df_varnames %>%
                     dplyr::filter(var == cat_var1))$var_name
cat_var_name2 = (df_varnames %>%
                     dplyr::filter(var == cat_var2))$var_name
cat_var_name = paste0(cat_var_name1, " grouped by ", cat_var_name2)

# Deal with NA:
df[which(is.na(df[cat_var2])), cat_var2] = "NA"

# Frequencies within each level of the first variable:
df_plot = df %>%
    xtabs(formula = ~ eval(parse(text = cat_var1)) + eval(parse(text = cat_var2)) ) %>%
    as.data.frame()
names(df_plot) = c("var1", "var2", "freq")

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
p = plot_ly(
    data = df_plot,
    x = ~var2,
    y = ~freq,
    type = "bar",
    color = ~var1,
    colors = my_palette(nrow(df_plot)),
    text = ~var1,
    hovertemplate = paste0("<b>Frequency: %{y:,}<br>", 
                           cat_var_name2, ": %{x}<br>", 
                           cat_var_name1, ": %{text}</b><extra></extra>")
) %>%
    layout(
        xaxis = list(
            title = paste0("<b>", cat_var_name2, "</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18),
            categoryorder = "array"
        ),
        yaxis = list(
            title = "<b>Frequency<b>",
            titlefont = list(size = 20),
            tickfont = list(size = 18),
            type = "log"
        ),
        margin = list(
            l = 5,
            r = 70,
            t = 5,
            b = 70
        ),
        legend = list(
            title = list(
                text = paste0("<br><b>", cat_var_name1, "</b>"),
                font = list(size = 18)
            )
        ),
        hoverlabel = list(font = list(size = 16)),
        showlegend = TRUE
    )

p



