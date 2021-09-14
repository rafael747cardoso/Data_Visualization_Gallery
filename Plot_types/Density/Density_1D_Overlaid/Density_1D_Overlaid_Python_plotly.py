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
x_var = "sy_bmag"
x_var_name = df_varnames.loc[(df_varnames["var"] == x_var), ["var_name"]].values[0][0]
color_var = "disc_locale"
color_var_name = df_varnames.loc[(df_varnames["var"] == color_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[x_var, color_var]]

# Plot:
lvls = df_plot[color_var].unique()
n_levels = len(lvls)
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/n_levels) for i in np.array(range(n_levels))]]

hist_data_list = []
for l, lvl in enumerate(lvls):
    df_lvl = df_plot.loc[df_plot[color_var] == lvl, ]
    df_lvl = df_lvl.dropna()
    hist_data_list += [df_lvl[x_var].tolist()]

fig = ff.create_distplot(
    hist_data = hist_data_list,
    group_labels = lvls,
    curve_type = "kde",
    show_curve = True,
    show_hist = False,
    show_rug = False,
    colors = my_palette
)
fig.update_traces(
    hovertemplate = "<b>Density: %{y:,}<br>" +
                    x_var_name + ": %{x:,}</b>"
)
fig.update_layout(
    barmode = "overlay",
    xaxis_title = "<b>" + x_var_name + "</b>" ,
    yaxis_title = "<b>Density</b>",
    font = dict(
        size = 18
    ),
    showlegend = True,
    legend_title_text = "<b>" + color_var_name + "</b>",
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    )
)
fig.show()


