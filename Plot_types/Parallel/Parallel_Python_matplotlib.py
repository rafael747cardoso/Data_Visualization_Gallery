
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.path import Path
import matplotlib.patches as patches

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
# my_vars = ["pl_letter", "discoverymethod", "disc_locale", "pl_orbper", "st_teff",
#                "st_metratio", "sy_gaiamag", "dec"]
my_vars = ["pl_orbper", "st_teff", "sy_gaiamag", "disc_locale"]
my_vars_names = df_varnames.loc[df_varnames["var"].isin(my_vars)].copy()["var_name"].values.tolist()

# Adapt the data:
df_plot = df[numcat_vars]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop = True)

# Plot:
n_levels = 100
my_colors = ["#F41E1E", "#F4951E", "#F4F01E", "#4EF41E", "#1EF4DC", "#1E3CF4", "#F41EF3"]
cmap = LinearSegmentedColormap.from_list("my_palette", my_colors)
my_palette = [cmap(i/n_levels) for i in np.array(range(n_levels))]


ys = df_plot




iris = datasets.load_iris()
ynames = iris.feature_names
ys = iris.data
ymins = ys.min(axis=0)
ymaxs = ys.max(axis=0)
dys = ymaxs - ymins
ymins -= dys * 0.05  # add 5% padding below and above
ymaxs += dys * 0.05

ymaxs[1], ymins[1] = ymins[1], ymaxs[1]  # reverse axis 1 to have less crossings
dys = ymaxs - ymins

# transform all data to be compatible with the main axis
zs = np.zeros_like(ys)
zs[:, 0] = ys[:, 0]
zs[:, 1:] = (ys[:, 1:] - ymins[1:]) / dys[1:] * dys[0] + ymins[0]

fig, host = plt.subplots(figsize=(10,4))

axes = [host] + [host.twinx() for i in range(ys.shape[1] - 1)]
for i, ax in enumerate(axes):
    ax.set_ylim(ymins[i], ymaxs[i])
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    if ax != host:
        ax.spines['left'].set_visible(False)
        ax.yaxis.set_ticks_position('right')
        ax.spines["right"].set_position(("axes", i / (ys.shape[1] - 1)))

host.set_xlim(0, ys.shape[1] - 1)
host.set_xticks(range(ys.shape[1]))
host.set_xticklabels(ynames, fontsize=14)
host.tick_params(axis='x', which='major', pad=7)
host.spines['right'].set_visible(False)
host.xaxis.tick_top()
host.set_title('Parallel Coordinates Plot — Iris', fontsize=18, pad=12)

colors = plt.cm.Set2.colors
legend_handles = [None for _ in iris.target_names]
for j in range(ys.shape[0]):
    # create bezier curves
    verts = list(zip([x for x in np.linspace(0, len(ys) - 1, len(ys) * 3 - 2, endpoint=True)],
                     np.repeat(zs[j, :], 3)[1:-1]))
    codes = [Path.MOVETO] + [Path.CURVE4 for _ in range(len(verts) - 1)]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=2, alpha=0.7, edgecolor=colors[iris.target[j]])
    legend_handles[iris.target[j]] = patch
    host.add_patch(patch)
host.legend(legend_handles, iris.target_names,
            loc='lower center', bbox_to_anchor=(0.5, -0.18),
            ncol=len(iris.target_names), fancybox=True, shadow=True)
plt.tight_layout()






