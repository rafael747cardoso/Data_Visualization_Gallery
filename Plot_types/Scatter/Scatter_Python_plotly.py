
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap, to_hex

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
x_var = "sy_pm"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var = "st_mass"
y_var_name = df_varnames.loc[(df_varnames["var"] == y_var), ["var_name"]].values[0][0]
color_var = "disc_locale"
color_var_name = df_varnames.loc[(df_varnames["var"] == color_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, y_var, color_var]].copy()

# Plot:
lvls = df_plot[color_var].unique()
n_levels = len(lvls)
my_palette = ["#c70039", "#2a7b9b", "#eddd53"]

fig = go.Figure()
for l, lvl in enumerate(lvls):
    fig.add_trace(
        go.Scatter(
            x = df_plot[x_var][df_plot[color_var] == lvl],
            y = df_plot[y_var][df_plot[color_var] == lvl],
            mode = "markers",
            marker = {
                "size": 7,
                "color": my_palette[l]
            },
            name = lvl,
            hovertemplate =  "<b>" + x_var_name + ": %{x:}<br>" +
                             y_var_name + ": %{y:}<br>" + 
                             color_var_name + ": " + lvl + 
                             "</b><extra></extra>"
        )
    )
fig.update_layout(
    xaxis_title = "<b>" + x_var_name + "</b>" ,
    yaxis_title = "<b>" + y_var_name + "</b>",
    font = dict(
        size = 18
    ),
    showlegend = True,
    legend_title_text = "<b>" + color_var_name + "</b>",
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 20,
        font_family = "Rockwell"
    )
)
fig.show()


