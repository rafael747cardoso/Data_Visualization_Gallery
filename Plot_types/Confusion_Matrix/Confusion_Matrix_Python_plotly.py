
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap, to_hex
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
n_colors = 100
my_colors = ["#540A5C", "#E008F8", "#F81D08", "#F88A08"]
cmap = LinearSegmentedColormap.from_list("my_palette", my_colors)
my_palette = [to_hex(j) for j in  [cmap(i/n_colors) for i in np.array(range(n_colors))]]

fig = go.Figure(
    data = [
        go.Heatmap(
            x = x_vals,
            y = y_vals,
            z = cm,
            colorscale = my_palette,
            hoverinfo = "none",
            colorbar = dict(
                title = "<b>Counts</b>"
            )
        )
    ]
)
for x_ind, x_val in enumerate(x_vals):
    for y_ind, y_val in enumerate(y_vals):
        fig.add_annotation(
            x = x_val,
            y = y_val,
            text = str(cm[y_ind, x_ind]),
            showarrow = False,
            font = {
                "color": "white",
                "size": 30
            }
        )
fig.update_layout(
    height = 800,
    width = 800,
    xaxis_title = "<b>Predicted</b>" ,
    yaxis_title = "<b>Actual</b>",
    font = dict(
        size = 18
    ),
    plot_bgcolor = "white",
    xaxis = {
        "tickmode": "array",
        "tickvals" : x_vals
    },
    yaxis = {
        "tickmode": "array",
        "tickvals": y_vals
    }
)
fig.show()


