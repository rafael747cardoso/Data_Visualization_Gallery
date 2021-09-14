
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

# Adapt the data:
x_vals = df[x_var].tolist()

# Plot:
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
_ = sns.kdeplot(
    x = x_vals,
    color = "#813DDA",
    shade = True,
    alpha = 0.7,
    linewidth = 2,
    ax = ax,
    clip = (min(x_vals), max(x_vals)),
    bw_method = 0.3
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
plt.legend(
    [], [], 
    frameon = False
)

