
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
num_vars = ["sy_snum", "sy_pnum", "disc_year", "pl_orbeccen", "st_teff", "st_mass", "sy_pm",
            "sy_dist", "sy_gaiamag"]
num_vars_names = df_varnames.loc[df_varnames["var"].isin(num_vars)].copy()["var_name"].values

# Adapt the data:
df_plot = df[num_vars]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop = True)
df_plot = df_plot.corr()

# Plot:
my_colors = ["#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04"]
my_palette = LinearSegmentedColormap.from_list("my_palette", my_colors)

fig, ax = plt.subplots(
    figsize = (11, 10),
    tight_layout = True
)
_ = sns.heatmap(
    data = df_plot,
    cbar = True,
    cmap = my_palette,
    cbar_kws = {"label": "Pearson correlation"},
    square = True,
    xticklabels = num_vars_names,
    yticklabels = num_vars_names,
    ax = ax
)
_ = ax.invert_yaxis()
_ = ax.tick_params(
    axis = "x", 
    which = "major", 
    labelsize = 16
)
_ = plt.setp(
    ax.get_xticklabels(),
    rotation = 20,
    ha = "right",
    rotation_mode = "anchor"
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)


