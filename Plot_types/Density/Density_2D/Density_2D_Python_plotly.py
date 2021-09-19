
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
x_var = "sy_vmag"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var = "sy_jmag"
y_var_name = df_varnames.loc[(df_varnames["var"] == y_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, y_var]]

# Deal with nan:
df_plot = df_plot.dropna()

# Plot:
my_colors = ["#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04"]
fig = go.Figure(
    data = [
        go.Histogram2dContour(
            x = df_plot[x_var],
            y = df_plot[y_var],
            colorscale = my_colors,
            ncontours = 6,
            histnorm = "probability density",
            hovertemplate = "<b>" +
                            x_var_name + ": %{x:,}<br>" +
                            y_var_name + ": %{y:,}</br>" +
                            "Density: %{z:, }</b><extra></extra>",
            colorbar = dict(
                title = "<b>Density</b>"
            )
        )
    ]
)
fig.update_layout(
    height = 800,
    width = 800,
    xaxis_title = "<b>" + x_var_name + "</b>" ,
    yaxis_title = "<b>" + y_var_name + "</b>",
    font = dict(
        size = 18
    ),
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    )
)
fig.show()


