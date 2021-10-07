
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(geojsonio, lib = path_lib)
require(rjson, lib = path_lib)
require(rmapshaper, lib = path_lib)
require(leaflet, lib = path_lib)
require(htmltools, lib = path_lib)

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
shp_data@data = shp_data@data %>%
                    dplyr::left_join(df_data,
                                     by = structure(names = id_var,
                                                    .Data = id_var))

# Map:
vals = shp_data@data[, eval(color_var)]
labels = sprintf(paste0("<strong>ZIP code: %s<br/>Population: %g</strong>"),
                 shp_data@data[, id_var], vals) %>%
             lapply(htmltools::HTML)

scale = "linear"
if(scale == "linear"){
    bins_limits = seq(from = min(vals),
                      to = max(vals),
                      length.out = 10)
}
if(scale == "log"){
    n = 9
    bins_limits = min(vals)
    points = sort(vals)
    n_points = length(points)
    n_points_bin = n_points/n
    n_points_bins = trunc(seq(from = n_points_bin,
                              to = n_points,
                              length.out = n))
    cont = 0
    for(i in 1:n_points){
        cont = cont + 1
        if(cont %in% n_points_bins){
            bins_limits = c(bins_limits, points[i])
        }
    }
}
if(vals[1]%%1 == 0 &
   vals[round(length(vals)/2, 0)]%%1 == 0 &
   vals[length(vals)]%%1 == 0){
    bins_limits = round(bins_limits, 0)
}
repeated = bins_limits %>%
               duplicated() %>%
               which()
if(length(repeated) > 0){
    if(length(bins_limits) - length(repeated) > 2){
        bins_limits = bins_limits[-repeated]
    } else{
        bins_limits = seq(from = min(vals),
                          to = max(vals),
                          length.out = 10)
    }
}
pal = colorBin(palette = "YlOrRd",
               domain = vals,
               bins = bins_limits)

map = leaflet(shp_data) %>%
    setView(
        lng = 9.5,
        lat = 51.5,
        zoom = 5
    ) %>%
    addTiles(
        urlTemplate = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attribution = paste0('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap',
                             '</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')
    ) %>%
    addPolygons(
        fillColor = ~pal(eval(parse(text = color_var))),
        weight = 0,
        opacity = 1,
        color = "white",
        dashArray = "3",
        fillOpacity = 0.8,
        highlight = highlightOptions(
            sendToBack = TRUE,
            weight = 3,
            color = "#666",
            dashArray = "",
            fillOpacity = 0.9,
            bringToFront = TRUE
        ),
        label = labels,
        labelOptions = labelOptions(
            style = list(
                "font-weight" = "normal",
                padding = "3px 8px"
            ),
            textsize = "15px",
            direction = "auto"
        )
    ) %>%
    leaflet::addLegend(
        pal = pal,
        values = ~get(color_var),
        opacity = 0.7,
        position = "bottomright",
        title = "Population"
    ) %>%
    addControl(
        tags$h3(
            HTML("<b>Germany ZIP codes</b>")
        ),
        position = "bottomleft"
    )

map


