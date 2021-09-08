
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
x_var = "sy_vmag"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var = "sy_jmag"
y_var_name = df_varnames.loc[(df_varnames["var"] == y_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, y_var]]

# Deal with nan:
df_plot = df_plot.dropna()

# Plot:
n_binsxy = 150
my_palette = LinearSegmentedColormap.from_list("my_palette",
                                               ["#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04"])

fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
(c, xh, yh, image) = ax.hist2d(
    x = df_plot[x_var],
    y = df_plot[y_var],
    bins = [n_binsxy, n_binsxy],
    cmap = my_palette,
    density = False
)
_ = ax.set_aspect("equal")
cbar = fig.colorbar(
    mappable = image,
    location = "right",
    fraction = 0.25
)
cbar.ax.set_ylabel(
    "Counts",
    rotation = 90,
    fontsize = 14,
    fontweight = "bold"
)
_ = ax.set_xlabel(
    x_var_name,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    y_var_name,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.tick_params(
    axis = "x", 
    which = "major", 
    labelsize = 16
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)


