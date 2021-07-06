
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
cat_var = "pl_tsystemref"
cat_var_name = (df_varnames %>%
                    dplyr::filter(var == cat_var))$var_name

# Adapt the data:
df_plot = df %>%
    dplyr::group_by(eval(parse(text = cat_var))) %>%
    dplyr::summarise(freq = n()) %>%
    as.data.frame() %>%
    dplyr::arrange(desc(freq))
names(df_plot)[1] = "level"

# Deal with NA:
df_plot$level[which(is.na(df_plot$level))] = "NA"

# Levels order:
df_plot$level = factor(x = df_plot$level,
                       levels = unique(df_plot$level))

# Relative frequency:
df_plot$freq_rel = round(df_plot$freq/sum(df_plot$freq)*100,
                         digits = 3)
df_plot$freq_rel_char = paste0(df_plot$freq_rel, "%")

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
p = plot_ly(
    data = df_plot,
    x = ~level,
    y = ~freq,
    type = "bar",
    text = ~freq_rel_char,
    texttemplate = "%{text}",
    textposition = "outside",
    textfont = list(size = 20,
                    color = my_palette(3)[2]),
    color = ~level,
    colors = my_palette(nrow(df_plot)),
    hovertemplate = "<b>Frequency: %{y:,}</b><extra></extra>"
) %>%
    layout(
        xaxis = list(
            title = paste0("<b>", cat_var_name, "</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18),
            categoryorder = "array"
        ),
        yaxis = list(
            title = "<b>Frequency</b>",
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
        hoverlabel = list(font = list(size = 16)),
        showlegend = FALSE
    )

p
    

