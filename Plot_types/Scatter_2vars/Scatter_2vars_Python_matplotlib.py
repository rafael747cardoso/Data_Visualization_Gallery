
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
num_var_x = "sy_dist"
num_var_x_name = df_varnames.loc[(df_varnames["var"] == num_var_x), ["var_name"]].values[0][0]
num_var_y_var = "sy_pm"
num_var_y_name = df_varnames.loc[(df_varnames["var"] == num_var_y_var), ["var_name"]].values[0][0]

cat_var = "disc_locale"
cat_var_name = df_varnames.loc[(df_varnames["var"] == cat_var), ["var_name"]].values[0][0]











