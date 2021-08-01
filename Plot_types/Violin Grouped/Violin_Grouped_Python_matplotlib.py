
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.colorbar import ColorbarBase
import matplotlib.gridspec as gridspec

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
cat_var1 = "st_metratio"
cat_var2 = "disc_locale"
cat_var_name1 = df_varnames.loc[(df_varnames["var"] == cat_var1), ["var_name"]].values[0][0]
cat_var_name2 = df_varnames.loc[(df_varnames["var"] == cat_var2), ["var_name"]].values[0][0]
num_var = "sy_dist"
num_var_name = df_varnames.loc[(df_varnames["var"] == num_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.loc[:, [cat_var1, cat_var2, num_var]]

# Deal with nan:
df_plot[cat_var1] = df_plot[cat_var1].fillna("NA")
df_plot[cat_var2] = df_plot[cat_var2].fillna("NA")

# Plot:
lvls1 = np.sort(df_plot[cat_var1].unique())
n_levels1 = len(lvls1)
lvls2 = np.sort(df_plot[cat_var2].unique())
n_levels2 = len(lvls2)
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_levels2) for i in np.array(range(n_levels2))]

fig, ax = plt.subplots(
    figsize = (20, 10),
    tight_layout = True
)

lvls_ok = []
for l1, lvl1 in enumerate(lvls1):
    for l2, lvl2 in enumerate(lvls2):
        edge_color = my_palette[l2]
        fill_color = my_palette[l2]
        vals = df_plot.loc[(df_plot.loc[:, cat_var1] == lvl1) &
                           (df_plot.loc[:, cat_var2] == lvl2), num_var].values
        vals = vals[~np.isnan(vals)]
        
        # Even:
        if n_levels2 % 2 == 0:
            middle = n_levels2/2 - 1
            delta = 1/(n_levels2 - 1)
            if l2 < middle + 1:
                posl1l2 = l1 - ((middle - l2)*delta + delta/2)*0.8
            else:
                posl1l2 = l1 + ((l2 - middle)*delta - delta/2)*0.8
        # Odd:
        else:
            middle = n_levels2//2
            delta = 0.3/(middle)
            if l2 < middle:
                posl1l2 = l1 - (middle - l2)*delta
            if l2 == middle:
                posl1l2 = l1
            if l2 > middle:
                posl1l2 = l1 + (l2 - middle)*delta
        print("l1 = " + str(l1) + ", l2 = " + str(l2) + ", posl1l2 = " + str(posl1l2))
        
        if len(vals) == 0:
            continue
        lvls_ok += [lvl1]

        vl = ax.violinplot(
            dataset = vals,
            positions = [posl1l2],
            widths = 1/n_levels2*0.8,
            showmeans = False, 
            showmedians = False,
            showextrema = False
        )
        for patch in vl["bodies"]:
            patch.set(
                color = edge_color,
                facecolor = fill_color,
                linewidth = 2,
                alpha = 1
            )
lvls_ok = [i for n, i in enumerate(lvls_ok) if i not in lvls_ok[:n]]
_ = ax.set_xticks(np.arange(0, len(lvls_ok)))
_ = ax.set_xticklabels(lvls_ok)
_ = ax.set_yscale("log")
_ = ax.legend(
    lvls2,
    fontsize = "large",
    title = cat_var_name2,
    title_fontsize = 16,
    loc = "upper right"
)
_ = ax.set_xlabel(
    cat_var_name1,
    fontsize = 16,
    fontweight = "bold"
)
_ = ax.set_ylabel(
    num_var_name,
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


