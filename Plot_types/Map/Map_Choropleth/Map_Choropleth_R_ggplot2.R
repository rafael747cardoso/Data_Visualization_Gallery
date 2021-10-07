
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(ggplot2, lib = path_lib)
require(geojsonio, lib = path_lib)
require(broom, lib = path_lib)

# Dataset:
df_data = readr::read_csv(paste0(path_data, "plz_einwohner.csv")) %>%
              as.data.frame()
df_geo = geojsonio::geojson_read(paste0(path_data, "plz-gebiete.shp/plz-gebiete.shp"),
                                 what = "sp")

# Variables:
color_var = "einwohner"
id_var = "plz"

# Adapt the data:
df_geo = df_geo[!duplicated(df_geo@data),]
df_geo = broom::tidy(df_geo,
                     region = id_var,
                     set_RGEOS_CheckValidity(2L))
df_geo = df_geo %>%
             dplyr::left_join(df_data,
                         by = c("id" = id_var))

# Map:
my_colors = c("#581845", "#900C3F", "#C70039", "#FF5733", "#FFC300")
my_palette = colorRampPalette(colors = my_colors)
color_bins = seq(from = 0,
                 to = max(df_geo[, color_var])*1.1,
                 by = 5000)

p = ggplot() +
    geom_polygon(
        data = df_geo,
        aes(
            x = long,
            y = lat,
            group = group,
            fill = eval(parse(text = color_var))
        ),
        color = "grey",
        size = 0.01
    ) +
    theme_void() +
    coord_map(
        projection = "mercator",
        xlim = c(3, 17),
        ylim = c(47, 55)
    ) +
    scale_fill_gradientn(
        colors = my_palette(100),
        na.value = "white",
        breaks = color_bins,
        limits = c(min(color_bins), max(color_bins)),
        guide = guide_colorbar(
            direction = "horizontal",
            barheight = unit(
                x = 10,
                units = "pt"
            ),
            barwidth = unit(
                x = 600,
                units = "pt"
            ),
            draw.ulim = FALSE,
            title.position = "top",
            title.hjust = 0.5,
            label.hjust = 0.5            
        )
    ) +
    theme(
        plot.title = element_text(
            size = 20,
            hjust = 0.5,
            color = "#4e4d47",
            margin = margin(
                b = 2,
                t = 2,
                l = 2,
                r = 2,
                unit = "pt"
            )
        ),
        legend.title = element_text(
            size = 16,
            color = "#4e4d47",
            margin = margin(
                b = 2,
                t = 2,
                l = 2,
                r = 2,
                unit = "pt"
            )
        ),
        legend.text = element_text(
            size = 13,
            color = "#4e4d47",
            margin = margin(
                b = 2,
                t = 2,
                l = 2,
                r = 2,
                unit = "pt"
            )
        ),
        legend.position = c(0.5, -0.07),
        legend.background = element_rect(
            fill = "white",
            color = NA
        ),
        panel.background = element_rect(
            fill = "white"
        ),
        plot.margin = margin(
            t = 5,
            r = 5,
            b = 100, 
            l = 5,
            unit = "pt"
        )
    ) +
    labs(
        title = "Germany ZIP codes",
        fill = "Population"
    )

p



