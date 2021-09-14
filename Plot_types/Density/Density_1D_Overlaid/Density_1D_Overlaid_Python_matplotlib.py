
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
x_var = "sy_bmag"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
color_var = "disc_locale"
color_var_name = df_varnames.loc[(df_varnames["var"] == color_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, color_var]]

# Deal with NaN:
df_plot = df_plot.dropna()

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
    x_vals = df_lvl[x_var].tolist()
    xs = np.linspace(min(x_vals), max(x_vals), 1000)
    density = gaussian_kde(x_vals)
    density.covariance_factor = lambda: 0.3
    density._compute_covariance()
    _ = ax.plot(
        xs,
        density(xs),
        linewidth = 2,
        color = my_palette[l],
        label = lvl
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
    "Density",
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.tick_params(
    axis = "x", 
    which = "major", 
    labelsize = 16
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)



