
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(tidyr, lib = path_lib)
require(maditr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(ggplot2, lib = path_lib)
require(ggpcp, lib = path_lib)

# Dataset:
df = readr::read_csv(paste0(path_data, "nasa_exoplanets.csv")) %>%
         as.data.frame()
attr(df, "spec") = NULL
df_varnames = readr::read_csv(paste0(path_data, "nasa_exoplanets_var_names.csv")) %>%
                  as.data.frame()
attr(df_varnames, "spec") = NULL

# Variables:
my_vars = c("discoverymethod", "pl_orbper", "st_teff", "disc_locale", "sy_gaiamag")
my_vars_names = c()
for(i in 1:length(my_vars)){
    my_vars_names = c(my_vars_names,
                      df_varnames$var_name[which(df_varnames$var == my_vars[i])])
}

# Adapt the data:
df_plot = df %>%
              dplyr::filter(pl_letter == "d")
df_plot = df_plot[, my_vars]
df_plot = df_plot %>% 
              tidyr::drop_na()

# Plot:
color_var_ind = 1
color_var = my_vars[color_var_ind]
num_colors = length(unique(df_plot[, color_var]))
my_colors = c("#F41E31", "#1EF459", "#F41EBE", "#6E1EF4", "#1E81F4", "#1EF4EC", "#E5F41E", "#F4A21E")
my_palette = colorRampPalette(colors = my_colors)

p = ggplot(
        data = df_plot,
        aes(
            vars = vars(1:length(my_vars))
        )
    ) +
    geom_pcp(
        aes(
            colour = eval(parse(text = color_var))
        ),
        alpha = 0.7,
        boxwidth = 0.1,
        method = "uniminmax"
    ) +
    geom_pcp_box() +
    scale_colour_manual(
        values = my_palette(num_colors),
        name = my_vars_names[color_var_ind]
    ) +
    geom_pcp_text(
        boxwidth = 0.1
    ) +
    theme(
        axis.text.x = element_text(
            size = 14,
            angle = 0,
            vjust = 1
        ),
        axis.text.y = element_text(
            size = 14
        ),
        axis.title.x = element_text(
            size = 15,
            face = "bold"
        ),
        axis.title.y = element_text(
            size = 15,
            face = "bold"
        ),
        legend.title = element_text(
            size = 14,
            face = "bold"
        ),
        legend.text = element_text(
            size = 12
        ),
        panel.background = element_rect(
            fill = "white"
        ),
        plot.margin = margin(
            t = 0,
            r = 5,
            b = 5, 
            l = 5,
            unit = "pt"
        )
    ) +
    xlab("Variables") +
    ylab("Scaled values")

p


