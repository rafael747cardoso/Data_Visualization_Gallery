
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
x_var = "sy_pm"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var = "st_mass"
y_var_name = df_varnames.loc[(df_varnames["var"] == y_var), ["var_name"]].values[0][0]
color_var = "disc_locale"
color_var_name = df_varnames.loc[(df_varnames["var"] == color_var), ["var_name"]].values[0][0]
size_var = "pl_orbeccen"
size_var_name = df_varnames.loc[(df_varnames["var"] == size_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, y_var, color_var, size_var]].copy()
df_plot = df_plot.dropna()
lvls = df_plot[color_var].unique()
n_levels = len(lvls)
my_palette = ["#c70039", "#2a7b9b", "#eddd53"]
df_palette = pd.DataFrame(
    {
        color_var: lvls,
        "color_hex": my_palette
    }
)
df_plot = pd.merge(left = df_plot,
                   right = df_palette,
                   how = "inner",
                   left_on = color_var,
                   right_on = color_var)

# Plot:
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
bubbles = ax.scatter(
    x = df_plot[x_var],
    y = df_plot[y_var],
    c = df_plot["color_hex"].tolist(),
    s = df_plot[size_var]*100,
    alpha = 0.5
)
legend1 = ax.legend(
    *bubbles.legend_elements(),
    loc = "center right",
    title = color_var_name,
    title_fontsize = 16,
    fontsize = "large"
)
_ = ax.add_artist(legend1)

handles, labels = bubbles.legend_elements(prop = "sizes")
legend2 = ax.legend(
    handles,
    labels,
    loc = "upper right",
    title = size_var_name,
    title_fontsize = 16,
    fontsize = "large"
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
    labelsize = 16,
    rotation = 20
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)


