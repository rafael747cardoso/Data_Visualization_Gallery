
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
_ = sns.scatterplot(
    x = X,
    y = Y,
    marker = "o",
    color = "#52A7DA",
    edgecolor = None,
    label = "Data",
    ax = ax
)
_ = sns.lineplot(
    x = X,
    y = y_fit,
    linewidth = 2,
    color = "#F51616",
    label = "Best fit",
    ci = None,
    ax = ax
)
_ = ax.fill_between(
    x = X,
    y1 = y_fit_up,
    y2 = y_fit_dw,
    color = "#5DDA52",
    alpha = 0.9,
    label = str(nstd) + " sigma confidence interval"
)
handles, labels = ax.get_legend_handles_labels()
leg = ax.legend(
    handles, labels,
    fontsize = "large",
    title_fontsize = 16,
    loc = "upper left"
)
_ = ax.set_xlabel(
    pred_var_name,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    resp_var_name,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.tick_params(
    axis = "x", 
    which = "major", 
    labelsize = 16
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)


