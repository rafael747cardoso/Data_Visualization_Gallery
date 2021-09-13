
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

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

# Deal with NaN:
df = df.dropna()

# Adapt the data:
x_vals = df[x_var].tolist()
xs = np.linspace(min(x_vals), max(x_vals), 1000)
density = gaussian_kde(x_vals)
density.covariance_factor = lambda : 0.3
density._compute_covariance()

# Plot:
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
_ = ax.plot(
    xs,
    density(xs),
    linewidth = 2,
    color = "#813DDA"
)
_ = ax.fill_between(
    x = xs,
    y1 = density(xs),
    color = "#CAAFEE"
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


