
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import squarify

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
cat_var = "discoverymethod"
cat_var_name = df_varnames.loc[(df_varnames["var"] == cat_var), ["var_name"]].values[0][0]
size_var = "sy_dist"
size_var_name = df_varnames.loc[(df_varnames["var"] == size_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[cat_var, size_var]]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop = True)
df_plot = df_plot.groupby(by = [cat_var],
                          as_index = False).mean()

# Plot:
fig = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
squarify.plot(
    sizes = df_plot[size_var],
    label = df_plot[cat_var],
    alpha = 0.8
)
plt.axis("off")




