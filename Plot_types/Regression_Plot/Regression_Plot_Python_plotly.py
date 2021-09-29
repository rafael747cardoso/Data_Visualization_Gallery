
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import curve_fit

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
resp_var = "pl_orbper"
resp_var_name = df_varnames.loc[(df_varnames["var"] == resp_var), ["var_name"]].values[0][0]
pred_var = "pl_orbsmax"
pred_var_name = df_varnames.loc[(df_varnames["var"] == pred_var), ["var_name"]].values[0][0]

# Adapt the data:
df = df[[pred_var, resp_var]]
df = df.dropna()
df = df.reset_index(drop = True)
df = df[(df[resp_var] < 25000) &
        (df[pred_var] < 20 )]
df = df.sort_values(by = pred_var)

# Fit function:
def kepler_orb(x, a):
    y = a*x**(1.5)
    return(y)

# Regression model:
X = df[pred_var]
Y = df[resp_var]
popt, pcov = curve_fit(f = kepler_orb,
                       xdata = X,
                       ydata = Y,
                       p0 = [1],
                       method = "lm")
popt = popt[0]
perr = np.sqrt(np.diag(pcov))[0]
nstd = 10
popt_up = popt + nstd*perr
popt_dw = popt - nstd*perr
y_fit = kepler_orb(x = X,
                   a = popt)
y_fit_up = kepler_orb(x = X,
                      a = popt_up)
y_fit_dw = kepler_orb(x = X,
                      a = popt_dw)

# Plot:
fig = go.Figure(
    data = [
        go.Scatter(
            x = X,
            y = Y,
            mode = "markers",
            marker = {
                "size": 10,
                "color": "#52A7DA"
            },
            hovertemplate = "<b>" + pred_var_name + ": %{x:}<br>" +
                            resp_var_name + ": %{y:}<br></b><extra></extra>",
            name = "Data"
        ),
        go.Scatter(
            x = X,
            y = y_fit_up,
            mode = "lines",
            line = {
                "width": 2,
                "color": "#5DDA52"
            },
            name = str(nstd) + " sigma confidence interval"
        ),
        go.Scatter(
            x = X,
            y = y_fit,
            fillcolor = "#5DDA52",
            fill = "tonexty",
            hovertemplate = "<b>" + pred_var_name + ": %{x:}<br>" +
                            resp_var_name + ": %{y:}<br></b><extra></extra>",
            showlegend = False
        ),
        go.Scatter(
            x = X,
            y = y_fit,
            mode = "lines",
            line = {
                "width": 2,
                "color": "#F51616"
            },
            hovertemplate = "<b>" + pred_var_name + ": %{x:}<br>" +
                            resp_var_name + ": %{y:}<br></b><extra></extra>",
            name = "Best fit"
        ),
        go.Scatter(
            x = X,
            y = y_fit_dw,
            mode = "lines",
            line = {
                "width": 2,
                "color": "#5DDA52"
            },
            fillcolor = "#5DDA52",
            fill = "tonexty",
            showlegend = False
        )
    ]
)
fig.update_layout(
    xaxis_title = "<b>" + pred_var_name + "</b>" ,
    yaxis_title = "<b>" + resp_var_name + "</b>",
    font = dict(
        size = 18
    ),
    showlegend = True,
    plot_bgcolor = "white",
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    )
)
fig.show()


