
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.express as px

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
cat_var1 = "discoverymethod"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var2 = "disc_locale"
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
size_var = "sy_dist"
size_var_name = df_varnames.loc[(df_varnames["var"] == size_var), ["var_name"]].values[0][0]
color_var = "st_mass"
color_var_name = df_varnames.loc[(df_varnames["var"] == color_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df[[cat_var1, cat_var2, size_var, color_var]]
df_plot = df_plot.dropna()
df_plot = df_plot.reset_index(drop = True)
df_plot = df_plot.groupby(by = [cat_var1, cat_var2],
                          as_index = False).mean()

# Plot:
customdata = list(df_plot.columns)
fig = px.treemap(
    data_frame = df_plot,
    path = [cat_var1, cat_var2],
    values = size_var,
    color = color_var,
    custom_data = customdata,
    color_continuous_scale = "viridis",
    color_continuous_midpoint = np.average(df[color_var],
                                           weights = df[size_var])
)
fig.layout.coloraxis.colorbar.title = "<b>Mean " + color_var_name + "</b>"
fig.update_traces(
    hovertemplate = "<b>" + cat_var_name1 + " = </b>%{customdata[0]}<br>" +
                    "<b>" + cat_var_name2 + " = </b>%{customdata[1]}<br>" +
                    "<b>" + size_var_name + " = </b>%{customdata[2]:.2f}<br>" +
                    "<b>" + color_var_name + " = </b>%{customdata[3]:.2f}<br><extra></extra>"
)
fig.show()



