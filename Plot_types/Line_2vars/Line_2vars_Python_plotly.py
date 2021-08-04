
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
y_var_name = "Exoplanets discovered"

# Adapt the data:
df_plot = df.groupby(by = x_var)[x_var].agg("count")
df_plot = pd.DataFrame(
    {
        "x_var": df_plot.index.tolist(),
        "y_var": df_plot.values,
    }
)
df_plot = df_plot.sort_values("x_var")

# Plot:
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/3) for i in np.array(range(3))]]

fig = go.Figure(
    data = go.Scatter(
        x = df_plot["x_var"],
        y = df_plot["y_var"],
        mode = "lines+markers",
        line = {
            "width": 5,
            "color": my_palette[1]
        },
        marker = {
            "size": 10,
            "color": my_palette[1]
        },
        hovertemplate = "<b>" + x_var_name + ": %{x:}<br>" +
                        y_var_name + ": %{y:}<br>" +
                        "</b><extra></extra>"
    )
)
fig.update_layout(
    xaxis_title = "<b>" + x_var_name + "</b>" ,
    yaxis_title = "<b>" + y_var_name + "</b>",
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


