
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
num_vars = ["sy_snum", "sy_pnum", "disc_year", "pl_orbeccen", "st_teff", "st_mass", "sy_pm",
            "sy_dist", "sy_gaiamag"]
num_vars_names = df_varnames.loc[df_varnames["var"].isin(num_vars)].copy()["var_name"].values

# Adapt the data:
df_plot = df[num_vars]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop = True)
df_plot = df_plot.corr()

# Plot:
n_colors = 100
my_colors = ["#000000", "#E008F8", "#F81D08", "#F88A08", "#F7FE04"]
cmap = LinearSegmentedColormap.from_list("my_palette", my_colors)
my_palette = [to_hex(j) for j in  [cmap(i/n_colors) for i in np.array(range(n_colors))]]

fig = go.Figure(
    data = [
        go.Heatmap(
            x = num_vars_names,
            y = num_vars_names,
            z = df_plot,
            colorscale = my_palette,
            hovertemplate = "<b>" +
                            "%{x}<br>" +
                            "%{y}</br>" +
                            "Correlation: %{z:, }</b><extra></extra>",
            colorbar = dict(
                title = "<b>Pearson correlation </b>"
            )
        )
    ]
)
fig.update_layout(
    height = 900,
    width = 1200,
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


