
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(ggplot2, lib = path_lib)

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

# Deal with NA:
df_plot$level[which(is.na(df_plot$level))] = "NA"

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
df_plot = df_plot %>%
              dplyr::arrange(desc(level))
df_plot$freq_rel = round(df_plot$freq/sum(df_plot$freq)*100,
                         digits = 3)
df_plot$freq_rel_char = paste0(df_plot$freq_rel, "%")

# Create the y positons:
df_plot$ypos = cumsum(df_plot$freq_rel) - 0.5*df_plot$freq_rel

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
p = ggplot(
        data = df_plot,
        aes(
            x = "",
            y = freq_rel,
            fill = level
        )
    ) +
    geom_bar(
        stat = "identity",
        width = 1,
        color = "white"
    ) +
    coord_polar(
        theta = "y",
        start = 0
    ) +
    theme_void() +
    theme(legend.position = "none") +
    geom_text(
        aes(
            x = 1.7,
            y = ypos,
            label = level
        ),
        color = my_palette(3)[2],
        size = 6
    ) +
    geom_text(
        aes(
            x = 1.2,
            y = ypos,
            label = paste0(freq_rel_char, "\n(", freq, ")")
        ),
        color = "white",
        size = 4
    ) +
    scale_fill_manual(
        values = my_palette(nrow(df_plot))
    )

p


