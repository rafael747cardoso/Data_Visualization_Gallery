
# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

# Packages:
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Display options:
pd.set_option("display.width", 1200)
pd.set_option("display.max_columns", 300)
pd.set_option("display.max_rows", 300)

# Dataset:
df = pd.read_csv(path_data + "nasa_exoplanets.csv")
df_varnames = pd.read_csv(path_data + "nasa_exoplanets_var_names.csv")

# Variables:
cat_var = "pl_tsystemref"
cat_var_name = df_varnames.loc[(df_varnames["var"] == cat_var), ["var_name"]].values[0][0]

# Adapt the data:
df_plot = df.groupby(by = cat_var)[cat_var].agg("count")
levels = df_plot.index.tolist()
df_plot = pd.DataFrame({"level": levels,
                        "freq": df_plot.values.tolist()}).sort_values("freq",
                                                                      ascending = False)

# Deal with nan:
df_plot = df_plot.append(pd.DataFrame({"level": ["NA"],
                                       "freq": df[cat_var].isna().sum()}),
                        sort = False)
df_plot = df_plot.copy().reset_index(drop = True)

# Relative frequency:
df_plot["freq_rel"] = [round(i/sum(df_plot["freq"])*100, 3) for i in df_plot["freq"]]
df_plot["freq_rel_char"] = [str(i) + "%" for i in df_plot["freq_rel"]]

# Plot:
n_levels = df_plot.shape[0]
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [cmap(i/n_levels) for i in np.array(range(n_levels))]
fig = plt.figure(figsize = (20, 10),
                 tight_layout = True)
ax = sns.barplot(
    data = df_plot,
    x = "level",
    y = "freq",
    color = "level",
    dodge = False,
    palette = my_palette
)
ind = 0
for p in ax.patches:
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy() 
    ax.annotate(
        text = f'{df_plot["freq_rel_char"][ind]}',
        xy = (x + width/2, y + height*1.03),
        ha = "center",
        color = my_palette[n_levels//2],
        fontsize = 15
    )
    ind += 1
_ = ax.set_yscale("log")
_ = ax.set_xlabel(cat_var_name,
                  fontsize = 16)
_ = ax.set_ylabel("Frequency",
                  fontsize = 16)
_ = ax.tick_params(axis = "x", 
                   which = "major", 
                   labelsize = 16,
                   rotation = 20)
_ = ax.tick_params(axis = "y", 
                   which = "major", 
                   labelsize = 16)
plt.legend([],[], frameon = False)

