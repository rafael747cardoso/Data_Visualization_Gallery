
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
cat_var1 = "st_metratio"
cat_var2 = "disc_locale"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
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
lvls_ok = []
for l, lvl in enumerate(lvls):
    edge_color = my_palette[l]
    fill_color = my_palette[l]
    df_lvl = df_plot.loc[df_plot.loc[:, cat_var] == lvl, num_var].values
    df_lvl = df_lvl[~np.isnan(df_lvl)]
    if len(df_lvl) == 0:
        continue
    lvls_ok += [lvl]
    bp = ax.violinplot(
        dataset = df_lvl,
        positions = [l],
        widths = 0.5,
        showmeans = False, 
        showmedians = False,
        showextrema = False
    )
    for patch in bp["bodies"]:
        patch.set(
            color = edge_color,
            facecolor = fill_color,
            linewidth = 2,
            alpha = 1
        )
_ = ax.set_xticks(np.arange(1, len(lvls_ok) + 1))
_ = ax.set_xticklabels(lvls_ok)
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


