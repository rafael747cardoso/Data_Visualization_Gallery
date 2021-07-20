
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap, to_hex
from math import floor, ceil

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
num_var = "sy_dist"
num_var_name = df_varnames.loc[(df_varnames["var"] == num_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.loc[:, [cat_var, num_var]].sort_values(cat_var)

# Deal with nan:
df_plot[cat_var] = df_plot[cat_var].fillna("NA")

# Plot:
lvls = df_plot[cat_var].unique()
n_levels = len(lvls)
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/n_levels) for i in np.array(range(n_levels))]]
outlier_color = "#DA2E2E"
median_color = "#23C16A"

boxes = []
for l in range(n_levels):
    boxes += [
        go.Box(
            name = lvls[l],
            y = df_plot.loc[df_plot.loc[:, cat_var] == lvls[l], num_var].values,
            width = 0.4,
            boxpoints = "outliers",
            marker = {
                "outliercolor": outlier_color,
                "color": my_palette[l],
                "size": 7,
                "opacity": 0.5
            }
        )
    ]
fig = go.Figure(data = boxes)
fig.update_yaxes(
    type = "log"
)
fig.update_layout(
    xaxis_title = "<b>" + cat_var_name + "</b>" ,
    yaxis_title = "<b>" + num_var_name + "</b>",
    font = dict(
        size = 18
    ),
    showlegend = False,
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    )
)
fig.show()


