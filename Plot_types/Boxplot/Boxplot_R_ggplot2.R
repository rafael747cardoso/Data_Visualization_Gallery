
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
cat_var = "discoverymethod"
cat_var_name = (df_varnames %>%
                    dplyr::filter(var == cat_var))$var_name
num_var = "sy_dist"
num_var_name = (df_varnames %>%
                    dplyr::filter(var == num_var))$var_name

# Adapt the data:
df_plot = df %>%
              dplyr::select(cat_var,
                            num_var)

# Deal with NA:
df_plot[which(is.na(df_plot[, cat_var])), cat_var] = "NA"

# Levels order:
sorted_levels = sort(unique(df_plot[, cat_var]))
df_plot[, cat_var] = factor(x = df_plot[, cat_var],
                            levels = sorted_levels)


# df_plot = df_plot %>%
#              dplyr::filter(discoverymethod == "Transit")



# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))
outlier_color = "#DA2E2E"
median_color = "#23C16A"
n_levels = length(unique(df_plot[, cat_var]))
p = ggplot(
        data = df_plot,
        aes(
            x = get(cat_var),
            y = get(num_var),
            fill = get(cat_var),
            color = get(cat_var),
            stat = "identity"
        )
    ) +
    stat_boxplot(
        geom = "errorbar",
        show.legend = FALSE,
        width = 0.6
    ) +
    geom_boxplot(
        outlier.colour = outlier_color,
        outlier.alpha = 0.5,
        show.legend = FALSE,
        width = 0.6
    ) +
    coord_trans(
        y = "log10"
    ) +
    scale_y_continuous(
        breaks = breaks,
        limits = c(1, max(df_plot[, num_var], na.rm = TRUE))
    ) +
    stat_summary(
        geom = "crossbar",
        color = median_color,
        width = 0.6,
        fatten = 2,
        fun.data = function(x){c(y = median(x),
                                 ymin = median(x),
                                 ymax = median(x))},
        show.legend = FALSE
    ) +
    scale_fill_manual(
        values = my_palette(n_levels)
    ) +
    scale_color_manual(
        values = my_palette(n_levels)
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
    ylab(num_var_name)

p


