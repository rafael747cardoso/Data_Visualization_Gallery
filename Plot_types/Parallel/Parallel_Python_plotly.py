
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap, to_hex
from functools import reduce

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
my_vars = ["discoverymethod", "pl_orbper", "st_teff", "disc_locale", "sy_gaiamag"]
my_vars_names = reduce(pd.DataFrame.append,
                       map(lambda i: df_varnames[df_varnames["var"] == i], my_vars))
my_vars_names = my_vars_names["var_name"].values.tolist()

# Adapt the data:
df = df.loc[df["pl_letter"] == "d"]
df_plot = df[my_vars]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop = True)

# Plot:
vars_plots = []
for v, var in enumerate(my_vars):
    if df_plot[var].dtype.kind not in ["i", "u", "f"]:
        # Categorical variables:
        vals_unique = df_plot[var].unique()
        dic_var = dict([(val, c) for c, val in enumerate(vals_unique)])
        vars_plots += [
            dict(
                tickvals = [i for i in range(len(vals_unique))],
                ticktext = vals_unique,
                label = my_vars_names[v],
                values = [dic_var[i] for i in df_plot[var].tolist()]
            )
        ]
    else:
        # Numerical variables:
        vars_plots += [
            dict(
                range = [min(df_plot[var]), max(df_plot[var])],
                label = my_vars_names[v],
                values = df_plot[var]
            )
        ]

fig = go.Figure(
    data = [
        go.Parcoords(
            dimensions = list(vars_plots)
        )
    ]
)
fig.update_layout(
    font = dict(
        size = 18
    ),
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    ),
    margin = {
        "l": 250
    }
)
fig.show()


