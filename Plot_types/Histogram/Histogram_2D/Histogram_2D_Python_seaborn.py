
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
# To choose to palette params, use sns.choose_diverging_palette() in IPython notebook.
my_palette = sns.diverging_palette(h_neg = 278,
                                   h_pos = 63,
                                   s = 100,
                                   l = 50,
                                   sep = 1,
                                   center = "light",
                                   as_cmap = True)
fig, ax = plt.subplots(
    figsize = (11, 10),
    tight_layout = True
)
_ = sns.histplot(
    data = df_plot,
    x = x_var,
    y = y_var,
    stat = "count",
    bins = (n_binsxy, n_binsxy),
    legend = True,
    cbar = True,
    thresh = -0.01,
    cbar_kws = {"label": "Counts"},
    cmap = my_palette,
    ax = ax
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


