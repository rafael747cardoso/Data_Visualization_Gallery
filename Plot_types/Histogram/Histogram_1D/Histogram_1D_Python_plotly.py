# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.graph_objects as go

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

# Adapt the data:
x_vals = df[x_var]

# Plot:
fig = go.Figure(
    data = [
        go.Histogram(
            x = x_vals,
            histfunc = "count",
            nbinsx = 100,
            marker_color = "#813DDA",
            opacity = 0.9
        )
    ]
)
fig.update_traces(
    hovertemplate = "<b>Counts: %{y:,}<br>" + 
                    x_var_name + ": %{x:,}</b><extra></extra>"
)
fig.update_layout(
    xaxis_title = "<b>" + x_var_name + "</b>" ,
    yaxis_title = "<b>Counts</b>",
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


