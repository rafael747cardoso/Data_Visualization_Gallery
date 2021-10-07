
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(plotly, lib = path_lib)
require(geojsonio, lib = path_lib)
require(rjson, lib = path_lib)
require(rmapshaper, lib = path_lib)

# Dataset:
df_data = readr::read_csv(paste0(path_data, "plz_einwohner.csv")) %>%
              as.data.frame()
shp_data = geojsonio::geojson_read(paste0(path_data, "plz-gebiete.shp/plz-gebiete.shp"),
                                   what = "sp")

# Variables:
color_var = "einwohner"
id_var = "plz"

# Adapt the data:
shp_data = shp_data[!duplicated(shp_data@data),]
shp_data = rmapshaper::ms_simplify(shp_data,
                                   keep = 0.001)
json_data = geojsonio::geojson_json(shp_data)
geo_data = rjson::fromJSON(json_data)
n_polys = length(geo_data$features)

# Map:
my_colors = c("#581845", "#900C3F", "#C70039", "#FF5733", "#FFC300")
my_palette = colorRampPalette(colors = my_colors)

p = plot_ly(
        type = "choropleth",
        geojson = geo_data,
        locations = df_data[, id_var],
        z = df_data[, color_var],
        text = df_data[, id_var],
        featureidkey = paste0("properties.", id_var),
        colors = my_palette(100),
        marker = list(
            line = list(
                width = 0
            )
        ),
        colorbar = list(
            title = "<b>Population</b>",
            len = 1
        ),
        hovertemplate = paste0("<b>ZIP code: %{text}<br>",
                               "Population: %{z}</b><extra></extra>")
    ) %>%
    layout(
        title = list(
            text = "<b>Germany ZIP codes</b>",
            titlefont = list(
                size = 20
            ),
            tickfont = list(
                size = 18
            )
        ),
        margin = list(
            l = 10,
            r = 10,
            t = 30,
            b = 10
        ),
        hoverlabel = list(
            font = list(
                size = 18
            )
        ),
        geo = list(
            fitbounds = "geojson",
            visible = FALSE,
            projection = list(
                type = "mercator"
            )
        )
    )

p


