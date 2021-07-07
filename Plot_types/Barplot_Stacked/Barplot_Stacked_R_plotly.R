
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
df_varnames = readr::read_csv(paste0(path_data, "nasa_exoplanets_var_names.csv")) %>%
    as.data.frame()

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

t = 1
freq_rel = c()
levels_var1 = levels(df_plot$var1)
levels_var2 = levels(df_plot$var2)
for(i in 1:length(levels_var2)){
    sum_level_var1 = df_plot %>%
                         dplyr::filter(var2 == levels_var2[i]) %>%
                         dplyr::select(freq) %>%
                         sum()
    for(j in 1:length(levels_var1)){
        freq_rel = c(freq_rel,
                     round(df_plot$freq[t]/sum_level_var1*100,
                           digits = 2))
        t = t + 1
    }
}
df_plot$freq_rel = freq_rel

my_palette = colorRampPalette(c("#111539", "#97A1D9"))
p = plot_ly(
    data = df_plot,
    x = ~var2,
    # y = ~freq, # absolute
    y = ~freq_rel, # relative
    type = "bar",
    color = ~var1,
    colors = my_palette(nrow(df_plot)),
    text = ~var1,
    hovertemplate = paste0(
        # "<b>Frequency: %{y:,}<br>", 
        "<b>Proportion: %{y:,} %<br>", 
        cat_var_name2, ": %{x}<br>", 
        cat_var_name1, ": %{text}</b><extra></extra>"
    )
) %>%
    layout(
        xaxis = list(
            title = paste0("<b>", cat_var_name2, "</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18),
            categoryorder = "array"
        ),
        yaxis = list(
            # title = "<b>Frequency<b>",
            title = "<b>Proportion (%)<b>",
            titlefont = list(size = 20),
            tickfont = list(size = 18)
        ),
        margin = list(
            l = 5,
            r = 70,
            t = 30,
            b = 70
        ),
        legend = list(
            title = list(
                text = paste0("<br><b>", cat_var_name1, "</b>"),
                font = list(size = 18)
            )
        ),
        hoverlabel = list(font = list(size = 16)),
        showlegend = TRUE,
        barmode = "stack"
    )

p



