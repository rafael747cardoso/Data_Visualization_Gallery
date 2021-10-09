
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
df_plot$level[which(is.na(df_plot$level))] = "NA"

# Levels order:
df_plot$level = factor(x = df_plot$level,
                       levels = unique(df_plot$level))

# Relative frequency:
df_plot$freq_rel = round(df_plot$freq/sum(df_plot$freq)*100,
                         digits = 3)
df_plot$freq_rel_char = paste0(df_plot$freq_rel, "%")
df_plot$freq_rel_cum = cumsum(df_plot$freq_rel)

# Deal with small categories:
max_cats_size = 97
df_plot1 = df_plot %>%
    dplyr::filter(freq_rel_cum < max_cats_size) %>%
    dplyr::select(level,
                  freq)
df_plot2 = data.frame(
    "level" = c("Others"),
    "freq" = c((df_plot %>%
                    dplyr::filter(freq_rel_cum >= max_cats_size))$freq %>%
                   sum())
)
df_plot = rbind(df_plot1,
                df_plot2)
df_plot$level = as.character(df_plot$level)
df_plot$freq_rel = round(df_plot$freq/sum(df_plot$freq)*100,
                         digits = 3)
df_plot$freq_rel_char = paste0(df_plot$freq_rel, "%")

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
p = plot_ly(
        data = df_plot,
        labels = ~level,
        values = ~freq,
        type = "pie",
        textposition = "inside",
        textinfo = "percent",
        insidetextfont = list(
            color = "#FFFFFF",
            size = 20
        ),
        text = paste0("<b>", cat_var_name, ": ", df_plot$level, 
                       "\nFrequency: ", formatC(x = df_plot$freq,
                                                digits = 0,
                                                big.mark = ","), "</b>"),
        hoverinfo = "text",
        marker = list(
            colors = my_palette(nrow(df_plot)),
            line = list(
                color = "#FFFFFF",
                width = 1)
        ),
        pull = 0.03,
        showlegend = TRUE
    ) %>% 
    layout(
        legend = list(
            title = list(
                text = cat_var_name,
                font = list(
                    size = 20
                )
            ),
            font = list(
                size = 18
            ),
            y = 0.9
        ),
        margin = list(
            t = 10,
            b = 10
        ),
        hoverlabel = list(
            font = list(
                size = 16
            )
        )
    )

p


