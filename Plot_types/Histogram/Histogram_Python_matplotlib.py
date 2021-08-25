
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
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
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
_ = ax.hist(
    x = x_vals,
    bins = 100,
    alpha = 0.9,
    histtype = "stepfilled",
    align = "mid",
    color = "#813DDA",
    density = False
)
_ = ax.set_xlabel(
    x_var_name,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    "Frequency",
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





