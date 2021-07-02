
# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.colorbar import ColorbarBase
import matplotlib.gridspec as gridspec
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
my_palette = [cmap(i/n_groups) for i in np.array(range(n_groups))]
fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)
n_bars = n_groups
total_width = 0.8
single_width = 0.9
bar_width = total_width/n_groups
bars = []
for i, (name, values) in enumerate(df_plot.iloc[:, 1:].items()):
    x_offset = (i - n_bars/2)*bar_width + bar_width/2
    for x, y in enumerate(values):
        bar = ax.bar(
            x = x + x_offset, 
            height = y, 
            width = bar_width*single_width, 
            color = my_palette[i]
        )
    bars.append(bar[0])
    ax.legend(bars, df_plot.iloc[:, 1:].keys())
_ = ax.set_xticks(np.arange(df_plot.shape[0]))
_ = ax.set_xticklabels(df_plot[cat_var2])
_ = ax.set_yscale("log")
_ = ax.set_xlabel(
    cat_vars_name,
    fontsize = 16
)
_ = ax.set_ylabel(
    "Frequency",
    fontsize = 16
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
_ = plt.setp(ax.get_xticklabels(),
             ha = "right", 
             rotation_mode = "anchor")


