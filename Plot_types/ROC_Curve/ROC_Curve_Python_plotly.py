
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap, to_hex
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
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

# ROC curve:
y_prob = model.predict_proba(x_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_true = y_test,
                                 y_score = y_prob)
auc = roc_auc_score(y_true = y_test,
                    y_score = y_prob)
df_plot = pd.DataFrame({"fpr": fpr.round(3),
                        "tpr": tpr.round(3),
                        "thresholds": thresholds.round(3)})

# Plot:
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/3) for i in np.array(range(3))]]

fig = go.Figure(
    data = [
        go.Scatter(
            x = df_plot["fpr"],
            y = df_plot["tpr"],
            mode = "lines",
            line = {
                "width": 5,
                "color": my_palette[1]
            },
            fill = "tozeroy",
            fillcolor = my_palette[2],
            hovertemplate = "<b>False positive rate: %{x:}<br>" +
                            "True positive rate: %{y:}<br></b><extra></extra>"
        ),
        go.Scatter(
            x = [0, 1],
            y = [0, 1],
            mode = "lines",
            line = {
                "width": 2,
                "color": "white",
                "dash": "dash"
            }
        )
    ]
)
fig.update_layout(
    height = 800,
    width = 800,
    title = "<b>AUC = " + str(round(auc, 3)) + "</b>",
    xaxis_title = "<b>False positive rate</b>" ,
    yaxis_title = "<b>True positive rate</b>",
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

