
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
cat_var1 = "pl_letter"
cat_var2 = "discoverymethod"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
variables = [cat_var1, cat_var2]

# Deal with NAN:
df[variables] = df[variables].fillna("NA")

# Plot parameters:
df_plot = df
df_plot = df_plot.sort_values(cat_var2)
n_groups = len(set(df_plot[cat_var1].values.tolist()))

# Absolute frequency plot:
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_groups) for i in np.array(range(n_groups))]
levels_var1 = pd.crosstab(df_plot[cat_var1], df_plot[cat_var2]).sort_values(by = cat_var1, ascending = True).index.tolist()
levels_var2 = list(set(df_plot[cat_var2]))
fig = plt.figure(
    figsize = (20, 10),
    tight_layout = True
)
ax = sns.countplot(
    data = df_plot, 
    x = cat_var2, 
    hue = cat_var1,
    hue_order = levels_var1,
    dodge = False,
    ec = "white",
    palette = my_palette
)
legend = ax.get_legend()
handles = legend.legendHandles
legend.remove()
_ = ax.legend(
    handles,
    levels_var1,
    fontsize = "large",
    title = cat_var_name1,
    title_fontsize = 16,
    loc = "upper right"
)
_ = ax.set_xlabel(
    cat_var_name2,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    "Frequency",
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
_ = plt.setp(
    ax.get_xticklabels(),
    ha = "right", 
    rotation_mode = "anchor"
)
_ = plt.xlim(
    left = -1,
    right = len(levels_var2) + 1
)

# Relative frequency:
cmap = LinearSegmentedColormap.from_list("my_palette", ["#97A1D9", "#111539"])
my_palette = [cmap(i/n_groups) for i in np.array(range(n_groups))]
levels_var1 = pd.crosstab(df_plot[cat_var1], df_plot[cat_var2]).sort_values(by = cat_var1, ascending = False).index.tolist()
levels_var2 = list(set(df_plot[cat_var2]))
fig = plt.figure(
    figsize = (20, 10),
    tight_layout = True
)
ax = sns.histplot(
    data = df_plot,
    x = cat_var2,
    hue = cat_var1,
    hue_order = levels_var1,
    stat = "probability",
    multiple = "fill",
    shrink = 0.8,
    palette = my_palette,
    alpha = 1
)
legend = ax.get_legend()
handles = legend.legendHandles
legend.remove()
_ = ax.legend(
    handles,
    levels_var1,
    fontsize = "large",
    title = cat_var_name1,
    title_fontsize = 16,
    loc = "upper right"
)
_ = plt.yticks(
    ticks = ax.get_yticks(), 
    labels = ["{:.0f}".format(a) for a in ax.get_yticks()*100]
)
_ = ax.set_xlabel(
    cat_var_name2,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    "Proportion (%)",
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
_ = plt.setp(
    ax.get_xticklabels(),
    ha = "right", 
    rotation_mode = "anchor"
)
_ = plt.xlim(
    left = -1,
    right = len(levels_var2) + 1
)


