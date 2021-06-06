
# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(ggplot2, lib = path_lib)

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
                       levels = c(unique(df_plot$level)[unique(df_plot$level) != "NA"],
                                  "NA"))
df_plot$freq_rel = paste0(round(df_plot$freq/sum(df_plot$freq)*100,
                                digits = 3), "%")

# Plot:
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
    geom_text(aes(x = level, 
                  y = freq, 
                  label = freq_rel),
              vjust = -0.2) +
    scale_fill_manual(
        values = colorRampPalette(c("#111539", "#97A1D9"))(nrow(df_plot))
    ) +
    theme(
        axis.text.x = element_text(
            size = 14,
            angle = 20, 
            hjust = 1,
            vjust = 1
        ),
        axis.text.y = element_text(size = 14),
        axis.title.x = element_text(size = 15),
        axis.title.y = element_text(size = 15),
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

# y-axis notation and scale:
great_number = 10000
great_distance = 100
min_non_zero = (df_plot %>%
                    dplyr::filter(freq > 0) %>%
                    dplyr::arrange(freq))$freq[1]
if(max(abs(range(df_plot$freq))) > great_number &
   max(df_plot$freq)/(min_non_zero) > great_distance){
    p = p +
        scale_y_continuous(labels = function(x) format(x, scientific = TRUE),
                           trans = "log10")
}
if(max(abs(range(df_plot$freq))) > great_number &
   max(df_plot$freq)/(min_non_zero) <= great_distance){
    p = p +
        scale_y_continuous(labels = function(x) format(x, scientific = TRUE))
}
if(max(abs(range(df_plot$freq))) <= great_number &
   max(df_plot$freq)/(min_non_zero) > great_distance){
    p = p +
        scale_y_continuous(trans = "log10")
}

p


