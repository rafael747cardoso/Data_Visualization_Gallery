
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
df_map = df_geo.merge(right = df_data,
                      how = "left",
                      left_on = "plz",
                      right_on = "plz")
color_var = "einwohner"

# Map:
my_colors = ["#EF9A9A", "#F04949", "#F10606"]
my_palette = LinearSegmentedColormap.from_list("my_palette", my_colors)

fig, ax = plt.subplots(
    figsize = (20, 10)
)
df_map.plot(
    column = color_var,
    categorical=False,
    cmap = my_palette,
    linewidth = 0.1,
    ax = ax,
    edgecolor = "0.8"
)
sm = plt.cm.ScalarMappable(
    cmap = my_palette,
    norm = plt.Normalize(
        vmin = df_map[color_var].min(),
        vmax = df_map[color_var].max()
    )
)
sm.set_array([])
cbar = fig.colorbar(
    mappable = sm,
    location = "bottom",
    orientation = "horizontal",
    fraction = 0.03,
    pad = 0.1,
    aspect = 30,
    format = "%.0f"
)
_ = cbar.ax.set_xlabel(
    "Population",
    fontsize = 14,
    fontweight = "bold",
    loc = "center"
)
_ = ax.axis("off")
_ = ax.set_title(
    "Germany ZIP codes",
    fontdict = {
        "fontsize": 20,
        "fontweight": 3
    }
)








