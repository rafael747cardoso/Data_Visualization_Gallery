
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
cat_var1 = "discoverymethod"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var2 = "pl_letter"
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
num_var = "sy_dist"
num_var_name = df_varnames.loc[(df_varnames["var"] == num_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.loc[:, [cat_var1, cat_var2, num_var]]
df_plot = df_plot.sort_values(cat_var1)

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
outlier_color = "#DA2E2E"
median_color = "#23C16A"
sns.boxplot(
    data = df_plot,
    x = cat_var1,
    y = num_var,
    color = cat_var2,
    hue = cat_var2,
    dodge = True,
    palette = my_palette,
    saturation = 1,
    ax = ax,
    flierprops = {
        "markerfacecolor": outlier_color,
        "markeredgecolor": outlier_color,
        "markersize": 5,
        "alpha": 0.5
    },
    width = 0.8
)

# Track the boxes that are ploted:
art_ind, l2_ind = [], []
cnt = 0
for l1, lvl1 in enumerate(lvls1):
    for l2, lvl2 in enumerate(lvls2):
        df_lvl = df_plot.loc[(df_plot.loc[:, cat_var1] == lvl1) & \
                             (df_plot.loc[:, cat_var2] == lvl2), num_var].values
        df_lvl = df_lvl[~np.isnan(df_lvl)]
        if len(df_lvl) > 0:
            art_ind += [cnt]
            l2_ind += [l2]
            cnt += 1
df_inds = pd.DataFrame(
    {
        "art_ind": art_ind,
        "l2_ind": l2_ind
    }
)
# Change their colors:
for i, artist in enumerate(ax.artists):
    l2 = df_inds.loc[df_inds["art_ind"] == i, "l2_ind"].tolist()[0]
    artist.set_edgecolor(my_palette[l2])
    artist.set_color(my_palette[l2])
    # Each of the box has 6 component lines:
    for j in range(i*6, i*6 + 6):
        line = ax.lines[j]
        # The 4th line is the median one:
        if j - i*6 == 4:
            line.set_color(median_color)
        else:
            line.set_color(my_palette[l2])
        line.set_linewidth(2)

plt.legend(
    title = cat_var_name2,
    fontsize = 12    
)
plt.setp(
    ax.get_legend().get_title(),
    fontsize = "14"
)
# Fix the borders in the legend items:
for i in range(n_levels2):
    _ = ax.get_legend().get_patches()[i].set_edgecolor("white")

_ = ax.set_yscale("log")
_ = ax.set_xlabel(
    cat_var_name1,
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


