
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
resp_var = "ttv_flag"
resp_var_name = df_varnames.loc[(df_varnames["var"] == resp_var), ["var_name"]].values[0][0]
pred_vars = ["sy_snum", "sy_pnum", "disc_year", "pl_orbeccen", "st_teff", "st_mass", "sy_pm",
            "sy_dist", "sy_gaiamag"]
pred_vars_names = df_varnames.loc[df_varnames["var"].isin(pred_vars)].copy()["var_name"].values.tolist()

# Adapt the data:
df_data = df[[resp_var] + pred_vars]
df_data = df_data.dropna()
df_data = df_data.reset_index(drop = True)

# Classification model:
x = df_data[pred_vars].values.reshape(-1, len(pred_vars))
y = df_data[resp_var].values
x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size = 0.7,
                                                    random_state = 42)
model = LogisticRegression(
    penalty = "l2",
    tol = 1E-4,
    C = 1,
    fit_intercept = True,
    random_state = 0,
    solver = "liblinear"
).fit(x_train, y_train)

# Confusion matrix:
cm = pd.DataFrame(
    data = confusion_matrix(y_true = y_test,
                            y_pred = model.predict(x_test)),
    index = [0, 1],
    columns = [0, 1]
)
x_vals = cm.index.tolist()
y_vals = cm.columns.tolist()
cm = cm.to_numpy()

# Plot:
my_colors = ["#540A5C", "#E008F8", "#F81D08", "#F88A08"]
my_palette = LinearSegmentedColormap.from_list("my_palette", my_colors)

fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
im = plt.imshow(
    X = cm,
    aspect = "equal",
    origin = "lower",
    cmap = my_palette
)
for i in range(len(x_vals)):
    for j in range(len(y_vals)):
        text = ax.text(
            j, i, cm[i, j],
            ha = "center",
            va = "center",
            color = "w",
            fontdict = {
                "fontsize": "20",
                "fontweight": "bold",
                "color": "white"
            }
        )
cbar = fig.colorbar(
    mappable = im,
    location = "right",
    fraction = 0.25
)
_ = cbar.ax.set_ylabel(
    "Counts",
    rotation = 90,
    fontsize = 14,
    fontweight = "bold"
)
_ = ax.set_xticks(
    ticks = np.arange(len(x_vals))
)
_ = ax.set_yticks(
    ticks = np.arange(len(y_vals))
)
_ = ax.set_xticklabels(
    labels = x_vals
)
_ = ax.set_yticklabels(
    labels = y_vals
)
_ = ax.set_xlabel(
    "Predicted",
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    "Actual",
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.tick_params(
    axis = "x", 
    which = "major", 
    labelsize = 16
)
_ = plt.setp(
    ax.get_xticklabels(),
    rotation = 0,
    ha = "center",
    rotation_mode = "anchor"
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)


