
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Colormap

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
x_var = "disc_year"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var = "sy_pnum"
y_var_name = df_varnames.loc[(df_varnames["var"] == y_var), ["var_name"]].values[0][0]
z_var = "sy_gaiamag"
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
    figsize = (11, 10),
    tight_layout = True
)
_ = sns.heatmap(
    data = z_vals,
    cbar = True,
    cmap = my_palette,
    cbar_kws = {"label": "Mean " + z_var_name},
    square = True,
    ax = ax
)
_ = plt.ylim(0, len(y_vals))
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



