
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import seaborn as sns
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
cmap = LinearSegmentedColormap.from_list("my_palette",
                                         ["#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04"])
my_palette = [cmap(i/n_binsxy) for i in np.array(range(n_binsxy))]

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
    ax = ax
)
_ = ax.collections[0].colorbar.set_label("Counts")
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


