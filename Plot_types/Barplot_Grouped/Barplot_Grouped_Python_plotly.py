
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
cat_var1 = "pl_letter"
cat_var2 = "discoverymethod"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
cat_vars_name = cat_var_name1 + " grouped by " + cat_var_name2
variables = [cat_var1, cat_var2]

# Deal with NAN:
df[variables] = df[variables].fillna("NA")

# Frequencies within each level of the first variable:
levels_var1 = df[cat_var1].unique().tolist()
levels_var2 = df[cat_var2].unique().tolist()
df_plot = pd.DataFrame({cat_var2: levels_var2})
for lvl_var1 in levels_var1:
    var2invar1 = df.loc[df[cat_var1] == lvl_var1][cat_var2].tolist()
    var2invar1_counts = [var2invar1.count(i) if var2invar1.count(i) > 0 else np.nan for i in levels_var2]
    lvl_var1_name = re.sub(pattern = r"[ \-()#/@;:<>{}=~|.?,\\]", 
                           repl = "_", 
                           string = lvl_var1)
    df_plot = pd.concat(
        [
            df_plot,
            pd.DataFrame({lvl_var1_name: var2invar1_counts},
                         dtype = "int")
        ],
        axis = 1)
df_plot = df_plot.fillna(0)

# Plot:
n_groups = df_plot.shape[1] - 1
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/n_groups) for i in np.array(range(n_groups))]]
bars = []
for i in range(n_groups):
    bars += [
        go.Bar(
            name = df_plot.columns[i + 1],
            x = df_plot[cat_var2],
            y = df_plot[df_plot.columns[i + 1]],
            marker = dict(color = my_palette[i]),
            offsetgroup = i
        )
    ]
fig = go.Figure(data = bars)
fig.update_yaxes(type = "log")
fig.update_layout(
    xaxis_title = "<b>" + cat_vars_name + "</b>" ,
    yaxis_title = "<b>Frequency</b>",
    legend_title = cat_var_name1,
    font = dict(size = 18),
    showlegend = True,
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    )
)
fig.show()


