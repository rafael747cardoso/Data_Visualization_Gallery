
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import scipy.stats as st

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
x_var = "sy_vmag"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var = "sy_jmag"
y_var_name = df_varnames.loc[(df_varnames["var"] == y_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, y_var]]

# Deal with nan:
df_plot = df_plot.dropna()

# Plot:
my_palette = LinearSegmentedColormap.from_list("my_palette",
                                               ["#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04"])

n_points = 100
X, Y = df_plot[x_var], df_plot[y_var]
xmin, xmax = min(X), max(X)
ymin, ymax = min(Y), max(Y)
xx, yy = np.mgrid[xmin:xmax:eval(str(n_points) + "j"), ymin:ymax:eval(str(n_points) + "j")]
positions = np.vstack([xx.ravel(), yy.ravel()])
values = np.vstack([X, Y])
kernel = st.gaussian_kde(values)
Z = np.reshape(kernel(positions).T, xx.shape)

fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
cs = ax.contourf(
    xx, yy, Z,
    cmap = my_palette,
    levels = 5
)
_ = ax.set_aspect("equal")
cbar = fig.colorbar(
    mappable = cs,
    location = "right",
    fraction = 0.25
)
cbar.ax.set_ylabel(
    "Density",
    rotation = 90,
    fontsize = 14,
    fontweight = "bold"
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
    labelsize = 16
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)


