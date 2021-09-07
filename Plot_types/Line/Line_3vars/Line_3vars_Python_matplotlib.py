
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
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
x_var = "disc_year"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var_name = "Exoplanets discovered"
color_var = "st_metratio"
color_var_name = df_varnames.loc[(df_varnames["var"] == color_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.groupby([x_var, color_var]).size().reset_index(name = "y_var")

# Plot:
lvls = df_plot[color_var].unique()
n_levels = len(lvls)
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_levels) for i in np.array(range(n_levels))]

fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
for l, lvl in enumerate(lvls):
    df_lvl = df_plot.loc[df_plot[color_var] == lvl, ]
    if df_lvl.shape[0] < 2:
        continue
    _ = ax.plot(
        df_lvl[x_var],
        df_lvl["y_var"],
        label = lvl,
        linewidth = 3,
        color = my_palette[l],
        alpha = 0.8
    )
_ = ax.legend(
    fontsize = "large",
    title = color_var_name,
    title_fontsize = 16,
    loc = "upper right"
)
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
    labelsize = 16,
    rotation = 20
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)


