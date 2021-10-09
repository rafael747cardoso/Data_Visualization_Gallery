
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(tidyr, lib = path_lib)
require(Hmisc, lib = path_lib)
require(reshape2, lib = path_lib)
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
num_vars = c("sy_snum", "sy_pnum", "disc_year", "pl_orbeccen", "st_teff", "st_mass", "sy_pm",
             "sy_dist", "sy_gaiamag")
num_vars_names = c()
for(i in 1:length(num_vars)){
    num_vars_names = c(num_vars_names,
                       df_varnames$var_name[which(df_varnames$var == num_vars[i])])
}

# Adapt the data:
df_plot = df[, num_vars]
df_plot = df_plot %>% 
              tidyr::drop_na()
df_plot = (df_plot %>%
              as.matrix() %>%
              rcorr(type = "pearson"))$r
df_plot = melt(data = df_plot,
               value.name = "Vars_corr")

# Plot:
my_colors = c("#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04")
my_palette = colorRampPalette(colors = my_colors)

p = ggplot(
        data = df_plot,
        aes(
            x = Var1,
            y = Var2,
            fill = Vars_corr
        )
    ) +
    geom_tile() +
    coord_fixed(
        ratio = 1
    ) +
    scale_fill_gradientn(
        colors = my_palette(100),
        na.value = "white",
        guide = guide_colorbar(
            direction = "vertical",
            barheight = unit(
                x = "500",
                units = "pt"
            ),
            draw.ulim = FALSE,
            title.position = "top",
            title.hjust = 0.5,
            label.hjust = 0.5            
        )
    ) +
    scale_x_discrete(
        labels = num_vars_names
    ) +
    scale_y_discrete(
        labels = num_vars_names
    ) +
    theme(
        legend.title = element_text(
            size = 15,
            face = "bold"
        ),
        legend.text = element_text(
            size = 13
        ),
        axis.text.x = element_text(
            size = 14,
            angle = 30,
            hjust = 1,
            vjust = 1
        ),
        axis.text.y = element_text(
            size = 14
        ),
        panel.background = element_rect(
            fill = "white"
        ),
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
    labs(
        x = "",
        y = "",
        fill = "Pearson correlation"
    )

p


