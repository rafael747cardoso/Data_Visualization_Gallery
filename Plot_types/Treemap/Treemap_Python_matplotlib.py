
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import viridis
from matplotlib.colors import Normalize
import squarify

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
cat_var = "discoverymethod"
cat_var_name = df_varnames.loc[(df_varnames["var"] == cat_var), ["var_name"]].values[0][0]
size_var = "sy_dist"
size_var_name = df_varnames.loc[(df_varnames["var"] == size_var), ["var_name"]].values[0][0]
color_var = "dec"
color_var_name = df_varnames.loc[(df_varnames["var"] == color_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[cat_var, size_var, color_var]]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop = True)
df_plot = df_plot.groupby(by = [cat_var],
                          as_index = False).mean()

min_val = df_plot[color_var].min()
max_val = df_plot[color_var].max()
norm = Normalize(vmin = min_val,
                 vmax = max_val)
cmap = viridis
my_colors = [cmap(norm(val)) for val in df_plot[color_var]]

# Plot:
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
_ = squarify.plot(
    sizes = df_plot[size_var],
    label = df_plot[cat_var],
    color = my_colors,
    alpha = 0.8,
    ax = ax
)
_ = plt.axis("off")
img = plt.imshow(
    X = [df_plot[color_var]],
    aspect = "auto",
    cmap = cmap
)
_ = img.set_visible(False)
cbar = fig.colorbar(
    mappable = img,
    location = "right",
    fraction = 0.1
)
_ = cbar.ax.set_ylabel(
    "Mean " + color_var_name,
    rotation = 90,
    fontsize = 14,
    fontweight = "bold"
)
_ = plt.title(
    label = "Labels: " + cat_var_name + "\n Sizes: Mean " + size_var_name,
    fontdict = {
        "fontsize": 16,
        "fontweight": "bold"
    },
    loc = "center"
)


