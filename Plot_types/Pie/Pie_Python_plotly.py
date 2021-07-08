
# Paths:
path_data = "data/"

# Packages:
import numpy as np
import pandas as pd
import plotly.express as px
from matplotlib.colors import LinearSegmentedColormap, to_hex

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
                                       "freq": df[cat_var].isna().sum()})).sort_values("freq", ascending = False)
df_plot = df_plot.copy().reset_index(drop = True)

# Deal with small categories:
df_plot["freq_rel"] = [i/sum(df_plot["freq"])*100 for i in df_plot["freq"]]
df_plot["freq_rel_cum"] = df_plot["freq_rel"].cumsum()
max_cats_size = 99.5
df_plot1 = df_plot.loc[df_plot.loc[:, "freq_rel_cum"] < max_cats_size, ["level", "freq"]]
df_plot2 = pd.DataFrame(
    {
        "level": ["Others"],
        "freq": [df_plot.loc[df_plot.loc[:, "freq_rel_cum"] >= max_cats_size, "freq"].sum()]
    }
)
df_plot = pd.concat([df_plot1,
                     df_plot2]).reset_index(drop = True)

# Plot:
n_levels = df_plot.shape[0]
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/n_levels) for i in np.array(range(n_levels))]]

fig = go.Figure(
    data = [
        go.Pie(
            labels = df_plot["level"],
            values = df_plot["freq"],
            marker = dict(colors = my_palette),
            hovertemplate = "<b>" + cat_var_name + ": %{label}<br>" +
                            "<b>Frequency: %{value}<br>" +
                            "</b><extra></extra>"
        )
    ]
)
fig.update_layout(
    legend_title = "<b>" + cat_var_name + "</b>",
    font = dict(
        size = 20
    ),
    hoverlabel = dict(
        font_size = 18,
        font_family = "Rockwell"
    ),
    showlegend = True,
    plot_bgcolor = "white"
)
fig.show()


