
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import PolyCollection

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
num_var = "sy_dist"
num_var_name = df_varnames.loc[(df_varnames["var"] == num_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.loc[:, [cat_var, num_var]].sort_values(cat_var)

# Deal with nan:
df_plot[cat_var] = df_plot[cat_var].fillna("NA")

# Plot:
lvls = df_plot[cat_var].unique()
n_levels = len(lvls)
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_levels) for i in np.array(range(n_levels))]
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
sns.violinplot(
    data = df_plot,
    x = cat_var,
    y = num_var,
    color = cat_var,
    hue = cat_var,
    dodge = False,
    palette = my_palette,
    saturation = 1,
    ax = ax,
    width = 0.4,
    inner = None
)
for i, art in enumerate(ax.get_children()):
    if isinstance(art, PolyCollection):
        art.set_edgecolor(my_palette[i])

_ = ax.set_yscale("log")
_ = ax.set_xlabel(
    cat_var_name,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    num_var_name,
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
plt.legend(
    [], [], 
    frameon = False
)


