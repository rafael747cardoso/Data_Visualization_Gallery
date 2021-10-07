
# Paths:
path_data = "data/"
path_map = "Plot_types/Map/Map_Choropleth/"

# Packages:
import numpy as np
import pandas as pd
import geopandas as gpd
import folium

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df_data = pd.read_csv(path_data + "plz_einwohner.csv", 
                      sep = ",",
                      dtype = {"plz": str,
                               "einwohner": int})
df_geo = gpd.read_file(path_data + "plz-gebiete.shp/plz-gebiete.shp",
                       dtype = {"plz": str})

# Adapt the data:
df_geo = df_geo.to_json()

color_var = "einwohner"
id_var = "plz"

# Map:
my_map = folium.Map(
    location = [51.5, 9.5],
    zoom_start = 5,
    tiles = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap' +
           '</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains = "abcd"
)
folium.Choropleth(
    geo_data = df_geo,
    data = df_data,
    columns = [id_var, color_var],
    key_on = "feature.properties." + id_var,
    fill_color = "OrRd",
    fill_opacity = 0.7,
    line_opacity = 0.2,
    line_weight = 0.3,
    legend_name = "Population",
    highlight = True
).add_to(my_map)
my_map.save(path_map + "map_folium.html")





