
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.express as px
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
cat_var1 = "st_metratio"
cat_var2 = "disc_locale"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
num_var = "sy_dist"
num_var_name = df_varnames.loc[(df_varnames["var"] == num_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.loc[:, [cat_var1, cat_var2, num_var]]

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

fig = go.Figure()
for l2, lvl2 in enumerate(lvls2):
    fig.add_trace(
        go.Violin(
            x = df_plot[cat_var1][df_plot[cat_var2] == lvl2],
            y = df_plot[num_var][df_plot[cat_var2] == lvl2],
            line_color = my_palette[l2],
            fillcolor = my_palette[l2],
            opacity = 1,
            points = False,
            box_visible = False,
            meanline_visible = False,
            spanmode = "hard",
            name = lvl2
        )
    )
fig.update_yaxes(
    type = "log"
)
fig.update_layout(
    xaxis_title = "<b>" + cat_var_name1 + "</b>" ,
    yaxis_title = "<b>" + num_var_name + "</b>",
    font = dict(
        size = 18
    ),
    showlegend = True,
    legend_title_text = "<b>" + cat_var_name2 + "</b>",
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    ),
    violingap = 0,
    violinmode = "group"
)
fig.show()


