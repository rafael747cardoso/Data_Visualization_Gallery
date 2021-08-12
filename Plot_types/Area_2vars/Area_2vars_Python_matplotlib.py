
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

# Adapt the data:
df_plot = df.groupby(by = x_var)[x_var].agg("count")
df_plot = pd.DataFrame(
    {
        "x_var": df_plot.index.tolist(),
        "y_var": df_plot.values,
    }
)
df_plot = df_plot.sort_values("x_var")

# Plot:
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/3) for i in np.array(range(3))]

fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
_ = ax.plot(
    df_plot["x_var"],
    df_plot["y_var"],
    marker = "o",
    markersize = 10,
    linewidth = 5,
    color = my_palette[1],
    alpha = 0.8
)
_ = ax.fill_between(
    x = df_plot["x_var"],
    y1 = df_plot["y_var"],
    color = my_palette[2]
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


