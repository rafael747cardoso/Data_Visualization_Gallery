
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
cat_var1 = "discoverymethod"
cat_var2 = "pl_tsystemref"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
cat_vars_name = cat_var_name2 + " grouped by " + cat_var_name1
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
    var2invar1_counts_rel = [round(i/np.nansum(var2invar1_counts)*100, 2) for i in var2invar1_counts]
    var2invar1_counts_rel_char = [np.nan if np.isnan(i) else str(i) + "%" for i in var2invar1_counts_rel]
    lvl_var1_name = re.sub(pattern = r"[ \-()#/@;:<>{}=~|.?,\\]", 
                           repl = "_", 
                           string = lvl_var1)
    df_plot = pd.concat(
        [
            df_plot,
            # Absolute frequency:
            pd.DataFrame({lvl_var1_name + "_freq": var2invar1_counts},
                         dtype = "int"),
            # Relative frequency:
            pd.DataFrame({lvl_var1_name + "_freq_rel": var2invar1_counts_rel},
                         dtype = "int"),
            pd.DataFrame({lvl_var1_name + "_freq_rel_char": var2invar1_counts_rel_char},
                         dtype = "int")
        ],
        axis = 1)

# Plot:
n_levels = df_plot.shape[0]
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_levels) for i in np.array(range(n_levels))]

x_location = np.arange(n_levels)
bar_width = 0.35
sinal = 1

fig, ax = plt.subplots(figsize = (20, 10),
                       tight_layout = True)
for lvl_var1 in levels_var1[0:1]:
    lvl_var1 = levels_var1[0]
    lvl_var1_name = re.sub(pattern = r"[ \-()#/@;:<>{}=~|.?,\\]",
                           repl = "_",
                           string = lvl_var1)
    _ = ax.bar(
        x = x_location + sinal*bar_width/2,
        height = df_plot[lvl_var1_name + "_freq"],
        color = my_palette
    )
    sinal = -sinal
    ax.bar_label(_, padding = 3)
    # ind = 0
    # for p in ax.patches:
    #     width = p.get_width()
    #     height = p.get_height()
    #     x, y = p.get_xy() 
    #     ax.annotate(
    #         text = f'{df_plot[lvl_var1_name + "_freq_rel_char"][ind]}',
    #         xy = (x + width/2, y + height*1.03),
    #         ha = "center",
    #         color = my_palette[n_levels//2],
    #         fontsize = 15
    #     )
    #     ind += 1
_ = ax.set_yscale("linear")
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






