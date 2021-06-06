
# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

# Packages:
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

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

# Relative frequency:
df_plot["freq_rel"] = [str(round(i/sum(df_plot["freq"])*100, 3)) + "%" for i in df_plot["freq"]]

# Plot:
cmap = mpl.colors.LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
fig, ax = plt.subplots(figsize = (20, 10))
_ = ax.bar(
    x = df_plot["level"],
    height = df_plot["freq"],
    color = [cmap(i) for i in np.array(range(1, df_plot.shape[0]))/10]    
)
_ = ax.text(
    x = df_plot["level"],
    y = df_plot["freq"] + 0.1*max(df_plot["freq"]),
    s = df_plot["freq_rel"].values
)
_ = ax.set_xlabel(cat_var_name)
_ = ax.set_ylabel("Frequency")
_ = ax.set_yscale("log")


