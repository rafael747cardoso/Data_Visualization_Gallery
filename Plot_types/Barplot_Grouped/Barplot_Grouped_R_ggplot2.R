
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

# Plot:
n_levels_var2 = df_plot$var2 %>%
                    unique() %>%
                    length()
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
p = ggplot(data = df_plot) + 
    geom_bar(
        aes(
            x = var2,
            y = freq,
            fill = var1
        ),
        width = 0.9,
        position = position_dodge(width = 1),
        stat = "identity",
        show.legend = TRUE
    ) +
    scale_fill_manual(
        name = cat_var_name1,
        values = my_palette(n_levels_var2)
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

# Y-axis notation and scale:
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

### fix the ggplot2 log10 scale for val = 0 and 1


