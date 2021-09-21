
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
x_var = "disc_year"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
y_var = "sy_pnum"
y_var_name = df_varnames.loc[(df_varnames["var"] == y_var), ["var_name"]].values[0][0]
z_var = "sy_gaiamag"
z_var_name = df_varnames.loc[(df_varnames["var"] == z_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, y_var, z_var]]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop=True)
z_vals = df_plot.pivot_table(index = y_var,
                             columns = x_var,
                             values = z_var,
                             aggfunc = np.mean)
x_vals = z_vals.columns.tolist()
y_vals = z_vals.index.tolist()

# Plot:
n_colors = 100
my_colors = ["#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04"]
cmap = LinearSegmentedColormap.from_list("my_palette", my_colors)
my_palette = [to_hex(j) for j in  [cmap(i/n_colors) for i in np.array(range(n_colors))]]

fig = go.Figure(
    data = [
        go.Heatmap(
            x = x_vals,
            y = y_vals,
            z = z_vals,
            colorscale = my_palette,
            hovertemplate = "<b>" +
                            x_var_name + ": %{x}<br>" +
                            y_var_name + ": %{y}</br>" +
                            "Mean " + z_var_name + ": %{z:, }</b><extra></extra>",
            colorbar = dict(
                title = "<b>Mean " + z_var_name + "</b>"
            )
        )
    ]
)
fig.update_layout(
    xaxis_title = "<b>" + x_var_name + "</b>" ,
    yaxis_title = "<b>" + y_var_name + "</b>",
    xaxis = {
        "tickmode": "linear",
        "type": "category",
        "scaleanchor": "x"
    },
    yaxis = {
        "tickmode": "linear",
        "type": "category",
        "scaleanchor": "y"
    },
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


