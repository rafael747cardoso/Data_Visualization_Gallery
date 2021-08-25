
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
x_vals = df[x_var]

# Plot:
fig = plt.figure(
    figsize = (20, 10),
    tight_layout = True
)
ax = sns.histplot(
    x = x_vals,
    bins = 100,
    stat = "count",
    color = "#813DDA",
    alpha = 0.9,
    kde = False
)
plt.rcParams["patch.edgecolor"] = "none"
_ = ax.set_xlabel(
    x_var_name,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    "Counts",
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

