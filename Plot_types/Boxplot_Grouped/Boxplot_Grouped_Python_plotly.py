
# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_hex
from matplotlib.colorbar import ColorbarBase
import matplotlib.gridspec as gridspec
import plotly.express as px
import plotly.graph_objects as go
import re

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
cat_var1 = "discoverymethod"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var2 = "pl_letter"
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
num_var = "sy_dist"
num_var_name = df_varnames.loc[(df_varnames["var"] == num_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.loc[:, [cat_var1, cat_var2, num_var]]
df_plot = df_plot.sort_values(cat_var1)

# Deal with nan:
df_plot[cat_var1] = df_plot[cat_var1].fillna("NA")
df_plot[cat_var2] = df_plot[cat_var2].fillna("NA")

# Plot:
lvls1 = np.sort(df_plot[cat_var1].unique())
n_levels1 = len(lvls1)
lvls2 = np.sort(df_plot[cat_var2].unique())
n_levels2 = len(lvls2)
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/n_levels2) for i in np.array(range(n_levels2))]]
outlier_color = "#DA2E2E"
median_color = "#23C16A"

boxes = []
for l2, lvl2 in enumerate(lvls2):
    df_lvl = df_plot[df_plot[cat_var2] == lvl2]
    df_lvl = df_lvl.dropna(axis = 0)
    boxes += [
        go.Box(
            name = lvl2,
            x = df_lvl[cat_var1],
            y = df_lvl[num_var],
            boxpoints = "outliers",
            marker = {
                "color": my_palette[l2],
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
    boxmode = "group",
    legend_title_text = cat_var_name2,
    xaxis_title = "<b>" + cat_var_name1 + "</b>" ,
    yaxis_title = "<b>" + num_var_name + "</b>",
    font = dict(
        size = 18
    ),
    showlegend = True,
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    )
)
fig.show()




