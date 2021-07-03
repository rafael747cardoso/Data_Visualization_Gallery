
# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.colorbar import ColorbarBase
import matplotlib.gridspec as gridspec
import re
import seaborn as sns

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
cat_var1 = "pl_letter"
cat_var2 = "discoverymethod"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
cat_vars_name = cat_var_name1 + " grouped by " + cat_var_name2
variables = [cat_var1, cat_var2]

# Deal with NAN:
df[variables] = df[variables].fillna("NA")

df_plot = df

# Plot:
n_groups = len(set(df_plot[cat_var1].values.tolist()))
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_groups) for i in np.array(range(n_groups))]
fig = plt.figure(
    figsize = (20, 10),
    tight_layout = True
)
ax = sns.countplot(
    data = df_plot, 
    x = cat_var2, 
    hue = cat_var1,
    ec = "white",
    palette = my_palette
)
_ = ax.set_yscale("log")
_ = ax.set_xlabel(
    cat_vars_name,
    fontsize = 16
)
_ = ax.set_ylabel(
    "Frequency",
    fontsize = 16
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
_ = plt.setp(ax.get_xticklabels(),
             ha = "right", 
             rotation_mode = "anchor")


