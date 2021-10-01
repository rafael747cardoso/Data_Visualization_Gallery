
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.path import Path
import matplotlib.patches as patches
from functools import reduce

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables (the first variable must be categoric):
my_vars = ["discoverymethod", "pl_orbper", "st_teff", "disc_locale", "sy_gaiamag"]
my_vars_names = reduce(pd.DataFrame.append,
                       map(lambda i: df_varnames[df_varnames["var"] == i], my_vars))
my_vars_names = my_vars_names["var_name"].values.tolist()

# Adapt the data:
df = df.loc[df["pl_letter"] == "d"]
df_plot = df[my_vars]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop = True)

# Convert to numeric matrix:
ym = []
dics_vars = []
for v, var in enumerate(my_vars):
    if df_plot[var].dtype.kind not in ["i", "u", "f"]:
        dic_var = dict([(val, c) for c, val in enumerate(df_plot[var].unique())])
        dics_vars += [dic_var]
        ym += [[dic_var[i] for i in df_plot[var].tolist()]]
    else:
        ym += [df_plot[var].tolist()]
ym = np.array(ym).T

# Padding:
ymins = ym.min(axis = 0)
ymaxs = ym.max(axis = 0)
dys = ymaxs - ymins
ymins -= dys*0.05
ymaxs += dys*0.05

# Reverse some axes for better visual:
axes_to_reverse = []
for a in axes_to_reverse:
    ymaxs[a], ymins[a] = ymins[a], ymaxs[a]
dys = ymaxs - ymins

# Adjust to the main axis:
zs = np.zeros_like(ym)
zs[:, 0] = ym[:, 0]
zs[:, 1:] = (ym[:, 1:] - ymins[1:])/dys[1:]*dys[0] + ymins[0]

# Colors:
n_levels = len(dics_vars[0])
my_colors = ["#F41E1E", "#F4951E", "#F4F01E", "#4EF41E", "#1EF4DC", "#1E3CF4", "#F41EF3"]
cmap = LinearSegmentedColormap.from_list("my_palette", my_colors)
my_palette = [cmap(i/n_levels) for i in np.array(range(n_levels))]

# Plot:
fig, host_ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
axes = [host_ax] + [host_ax.twinx() for i in range(ym.shape[1] - 1)]
for i, ax in enumerate(axes):
    ax.set_ylim(
        bottom = ymins[i],
        top = ymaxs[i]
    )
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.ticklabel_format(style = 'plain')
    if ax != host_ax:
        ax.spines.left.set_visible(False)
        ax.yaxis.set_ticks_position("right")
        ax.spines.right.set_position(
            (
                "axes",
                 i/(ym.shape[1] - 1)
             )
        )
host_ax.set_xlim(
    left = 0,
    right = ym.shape[1] - 1
)
host_ax.set_xticks(
    range(ym.shape[1])
)
host_ax.set_xticklabels(
    my_vars_names,
    fontsize = 14
)
host_ax.tick_params(
    axis = "x",
    which = "major",
    pad = 7
)
host_ax.spines.right.set_visible(False)
host_ax.xaxis.tick_top()
for j in range(ym.shape[0]):
    verts = list(zip([x for x in np.linspace(0, len(ym) - 1, len(ym)*3 - 2, 
                                             endpoint = True)],
                 np.repeat(zs[j, :], 3)[1: -1]))
    codes = [Path.MOVETO] + [Path.CURVE4 for _ in range(len(verts) - 1)]
    path = Path(verts, codes)
    color_first_cat_var = my_palette[dics_vars[0][df_plot.iloc[j, 0]]]
    patch = patches.PathPatch(
        path,
        facecolor = "none",
        lw = 2,
        alpha = 0.7,
        edgecolor = color_first_cat_var
    )
    host_ax.add_patch(patch)

dic_count = 0
for i, ax in enumerate(axes):
    if df_plot.iloc[:, i].dtype.kind not in ["i", "u", "f"]:
        dic_var_i = dics_vars[dic_count]
        ax.set_yticks(
            range(len(dic_var_i))
        )
        ax.set_yticklabels(
            [key_val for key_val in dics_vars[dic_count].keys()]
        )
        dic_count += 1




