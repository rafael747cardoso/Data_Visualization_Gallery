
# Packages:
require(ggplot2)
require(dplyr)

# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

# Dataset:
df = read.csv(paste0(path_data, "nasa_exoplanets.csv"),
              sep = ",")
df_varnames = read.csv(paste0(path_data, "nasa_exoplanets_var_names.csv"),
                       sep = ";")

# Variables:
cat_var = "discoverymethod"
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
na_separeted = TRUE
if(na_separeted){
    df_plot$level[which(df_plot$level == "")] = NA
} else{
    df_plot$level[which(df_plot$level == "")] = "NA"
}

# Levels order:
df_plot$level = factor(x = df_plot$level,
                       levels = unique(df_plot$level))
df_plot$freq_rel = paste0(round(df_plot$freq/sum(df_plot$freq)*100,
                                digits = 3), "%")

# Plot:
p = ggplot(data = df_plot) + 
    geom_bar(
        aes(
            x = level,
            y = freq,
            fill = freq
        ),
        stat = "identity",
        show.legend = FALSE
    ) +
    geom_text(aes(x = level, 
                  y = freq, 
                  label = freq_rel),
              vjust = -0.2) +
    scale_fill_gradient(
        low = "#97A1D9",
        high = "#111539"
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


