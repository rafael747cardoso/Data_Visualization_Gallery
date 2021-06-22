
# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

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
                                       "freq": df[cat_var].isna().sum()}),
                        sort = False)
df_plot = df_plot.copy().reset_index(drop = True)

# Relative frequency:
df_plot["freq_rel"] = [str(round(i/sum(df_plot["freq"])*100, 3)) + "%" for i in df_plot["freq"]]

# Plot:
n_levels = df_plot.shape[0]
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/n_levels) for i in np.array(range(n_levels))]]
fig = px.bar(
    data_frame = df_plot,
    x = "level",
    y = "freq",
    log_y = True,
    color = "level",
    color_discrete_sequence = my_palette,
    text = "freq_rel"
)
fig.update_traces(
    textposition = "outside",
    textfont_color = my_palette[n_levels//2],
    textfont_size = 15,
    hovertemplate = "<b>Frequency: %{y:,}</b><extra></extra>"
)
fig.update_layout(
    xaxis_title = "<b>" + cat_var_name + "</b>" ,
    yaxis_title = "<b>Frequency</b>",
    legend_title = "Legend Title",
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

