
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Colormap
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
my_palette = [cmap(i/3) for i in np.array(range(3))]

fig = plt.figure(
    figsize = (20, 10),
    tight_layout = True
)
ax = sns.lineplot(
    data = df_plot,
    x = "fpr",
    y = "tpr",
    linewidth = 3,
    color = my_palette[1],
    ci = None
)
_ = ax.fill_between(
    x = df_plot["fpr"],
    y1 = 0,
    y2 = df_plot["tpr"],
    color = my_palette[2]
)
ax = sns.lineplot(
    x = [0, 1],
    y = [0, 1],
    linewidth = 2,
    color = "white",
    linestyle = "--",
    alpha = 0.6,
    ci = None
)
_ = ax.set_aspect(
    aspect = "equal"
)
_ = ax.set_xlabel(
    "False positive rate",
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    "True positive rate",
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_title(
    "AUC = " + str(round(auc, 3)),
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.tick_params(
    axis = "x", 
    which = "major", 
    labelsize = 16,
    rotation = 20
)
_ = ax.tick_params(
    axis = "y", 
    which = "major", 
    labelsize = 16
)
plt.legend(
    [], [], 
    frameon = False
)


