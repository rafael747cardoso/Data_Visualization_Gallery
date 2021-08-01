
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
cat_var1 = "st_metratio"
cat_var2 = "disc_locale"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
num_var = "sy_dist"
num_var_name = df_varnames.loc[(df_varnames["var"] == num_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.loc[:, [cat_var1, cat_var2, num_var]]

# Deal with nan:
df_plot[cat_var1] = df_plot[cat_var1].fillna("NA")
df_plot[cat_var2] = df_plot[cat_var2].fillna("NA")

# Plot:
lvls1 = np.sort(df_plot[cat_var1].unique())
n_levels1 = len(lvls1)
lvls2 = np.sort(df_plot[cat_var2].unique())
n_levels2 = len(lvls2)
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_levels2) for i in np.array(range(n_levels2))]


fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
sns.violinplot(
    data = df_plot,
    x = cat_var1,
    y = num_var,
    color = cat_var2,
    hue = cat_var2,
    hue_order = pd.crosstab(df_plot[cat_var2], df_plot[cat_var1]).sort_values(by = cat_var2).index,
    scale = "width",
    dodge = True,
    palette = my_palette,
    saturation = 1,
    width = 0.4,
    inner = None,
    cut = 0,
    ax = ax
)
_ = ax.legend(
    fontsize = "large",
    title = cat_var_name2,
    title_fontsize = 16,
    loc = "upper right"
)
_ = ax.set_yscale("log")
_ = ax.set_xlabel(
    cat_var_name1,
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


