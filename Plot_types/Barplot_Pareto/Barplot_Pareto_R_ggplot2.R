
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
         as.data.frame() %>%
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

# Levels order:
df_plot$level = factor(x = df_plot$level,
                       levels = unique(df_plot$level))

# Relative frequency:
df_plot$freq_rel = round(df_plot$freq/sum(df_plot$freq)*100,
                         digits = 3)
df_plot$freq_rel_char = paste0(df_plot$freq_rel, "%")

# Cumulative frequency:
df_plot$freq_rel_cum = cumsum(df_plot$freq_rel)
df_plot$freq_rel_cum_char = paste0(df_plot$freq_rel_cum, "%")
df_plot$ind = 1:nrow(df_plot)

n = nrow(df_plot)
pareto_scale = df_plot$freq_rel_cum[n]/df_plot$freq[1]

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
p = ggplot(data = df_plot) + 
    geom_bar(
        aes(
            x = level,
            y = freq,
            fill = level
        ),
        stat = "identity",
        show.legend = FALSE
    ) +
    geom_text(
        aes(
            x = level, 
            y = freq, 
            label = freq_rel_char
        ),
        color = my_palette(3)[2],
        size = 5,
        vjust = -0.2
    ) +
    scale_fill_manual(values = my_palette(nrow(df_plot))) +
    geom_line(
        aes(
            x = ind,
            y = freq_rel_cum/pareto_scale
        ),
        color = "#FF7000",
        size = 1.5
    ) +
    geom_point(
        aes(
            x = ind,
            y = freq_rel_cum/pareto_scale
        ),
        color = "#FF7000",
        size = 2
    ) +
    geom_text(
        aes(
            x = level, 
            y = freq_rel_cum/pareto_scale, 
            label = freq_rel_cum_char
        ),
        color = "#FF7000",
        size = 5,
        vjust = 2
    ) +
    scale_y_continuous(
        sec.axis = sec_axis(
            trans = ~ .*pareto_scale,
            name = "Cumulative frequency"
        )
    ) +
    theme(
        axis.text.x = element_text(
            size = 14,
            angle = 20, 
            hjust = 1,
            vjust = 1
        ),
        axis.text.y = element_text(size = 14),
        axis.title.x = element_text(
            size = 15,
            face = "bold"
        ),
        axis.title.y = element_text(
            size = 15,
            face = "bold"
        ),
        panel.background = element_rect(fill = "white"),
        panel.grid.major = element_line(
            size = 0.2,
            linetype = "solid",
            colour = "#eaeaea"
        ),
        panel.grid.minor = element_line(
            size = 0.1,
            linetype = "solid",
            colour = "#eaeaea"
        ),
        plot.margin = margin(
            t = 0, 
            r = 5,
            b = 5, 
            l = 10,
            unit = "pt"
        )
    ) +
    xlab(cat_var_name) +
    ylab("Frequency")

p


