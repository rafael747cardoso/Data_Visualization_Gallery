# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.figure_factory as ff

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

# Deal with NaN:
df = df.dropna()

# Adapt the data:
x_vals = df[x_var].tolist()

# Plot:
fig = ff.create_distplot(
    hist_data = [x_vals],
    group_labels = ["x"],
    curve_type = "kde",
    show_curve = True,
    show_hist = False,
    show_rug = False,
    colors = ["#813DDA"]
)
fig.update_traces(
    hovertemplate = "<b>Density: %{y:,}<br>" + 
                    x_var_name + ": %{x:,}</b><extra></extra>"
)
fig.update_layout(
    xaxis_title = "<b>" + x_var_name + "</b>" ,
    yaxis_title = "<b>Density</b>",
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


