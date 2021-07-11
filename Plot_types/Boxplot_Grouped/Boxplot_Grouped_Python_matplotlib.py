
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.colorbar import ColorbarBase
import matplotlib.gridspec as gridspec

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
cat_var2 = "disc_locale"
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
num_var = "sy_dist"
num_var_name = df_varnames.loc[(df_varnames["var"] == num_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.loc[:, [cat_var, num_var]]




# Deal with nan:
df_plot[cat_var] = df_plot[cat_var].fillna("NA")

# Plot:
lvls = np.sort(df_plot[cat_var].unique())
n_levels = len(lvls)
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_levels) for i in np.array(range(n_levels))]
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
outlier_color = "#DA2E2E"
median_color = "#23C16A"

for l, lvl in enumerate(lvls):
    edge_color = my_palette[l]
    fill_color = my_palette[l]
    df_lvl = df_plot.loc[df_plot.loc[:, cat_var] == lvl, num_var].values
    df_lvl = df_lvl[~np.isnan(df_lvl)]
    bp = ax.boxplot(
        x = df_lvl,
        labels = [lvl],
        positions = [l],
        widths = 0.5,
        patch_artist = True
    )
    for patch in bp["boxes"]:
        patch.set(
            color = edge_color,
            facecolor = fill_color,
            linewidth = 2
        )
    for patch in bp["whiskers"]:
        patch.set(
            color = edge_color,
            linewidth = 2
        )
    for patch in bp["caps"]:
        patch.set(
            color = edge_color,
            linewidth = 2,
            xdata = patch.get_xdata() + (-0.1, 0.1)
        )
    for patch in bp["medians"]:
        patch.set(
            color = median_color,
            linewidth = 2
        )
    for patch in bp["fliers"]:
        patch.set(
            marker = "o",
            markeredgecolor = outlier_color,
            markerfacecolor = outlier_color,
            markersize = 5,
            alpha = 0.5
        )
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


