
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
from matplotlib.colors import LinearSegmentedColormap, to_hex

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

# Variables:
color_var = "einwohner"
id_var = "plz"

# Adapt the data:
df_geo = df_geo.drop_duplicates(subset = id_var,
                                keep = "first")
df_map = df_geo.merge(right = df_data,
                      how = "left",
                      left_on = id_var,
                      right_on = id_var)
df_map = df_map.set_index(id_var)

# Map:
n_colors = 50
my_colors = ["#581845", "#900C3F", "#C70039", "#FF5733", "#FFC300"]
cmap = LinearSegmentedColormap.from_list("my_palette", my_colors)
my_palette = [to_hex(j) for j in  [cmap(i/n_colors) for i in np.array(range(n_colors))]]
customdata = [color_var]

fig = px.choropleth(
    data_frame = df_map,
    geojson = df_map["geometry"],
    locations = df_map.index,
    color = color_var,
    color_continuous_scale = my_palette,
    custom_data = customdata,
    projection = "mercator"
)
fig.update_traces(
    hovertemplate = "<b>Population = </b>%{customdata[0]}<br>",
    marker_line_width = 0
)
fig.update_layout(
    title = {
        "text": "<b>Germany ZIP codes</b>",
        "x": 0.5,
        "y": 0.95,
        "xanchor": "center",
        "yanchor": "top"
    },
    coloraxis = {
        "colorbar": {
            "title": "<b>Population</b>"
        }
    },
    font = dict(
        size = 18
    ),
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    )
)
fig.update_geos(
    fitbounds = "locations",
    visible = False
)
fig.show(renderer = "browser")



