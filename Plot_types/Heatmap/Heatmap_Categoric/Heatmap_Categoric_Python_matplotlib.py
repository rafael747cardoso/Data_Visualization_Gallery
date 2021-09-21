
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
x_var = "st_metratio"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var = "discoverymethod"
y_var_name = df_varnames.loc[(df_varnames["var"] == y_var), ["var_name"]].values[0][0]
z_var = "pl_orbeccen"
z_var_name = df_varnames.loc[(df_varnames["var"] == z_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, y_var, z_var]]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop=True)
z_vals = df_plot.pivot_table(index = y_var,
                             columns = x_var,
                             values = z_var,
                             aggfunc = np.mean)
x_vals = z_vals.columns.tolist()
y_vals = z_vals.index.tolist()

# Plot:
my_colors = ["#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04"]
my_palette = LinearSegmentedColormap.from_list("my_palette", my_colors)

fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
im = plt.imshow(
    X = z_vals,
    aspect = "equal",
    origin = "lower",
    cmap = my_palette
)
cbar = fig.colorbar(
    mappable = im,
    location = "right",
    fraction = 0.25
)
_ = cbar.ax.set_ylabel(
    "Mean " + z_var_name,
    rotation = 90,
    fontsize = 14,
    fontweight = "bold"
)
_ = ax.set_xticks(
    ticks = np.arange(len(x_vals))
)
_ = ax.set_yticks(
    ticks = np.arange(len(y_vals))
)
_ = ax.set_xticklabels(
    labels = x_vals
)
_ = ax.set_yticklabels(
    labels = y_vals
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
_ = plt.setp(
    ax.get_xticklabels(),
    rotation = 45,
    ha = "right",
    rotation_mode = "anchor"
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)


