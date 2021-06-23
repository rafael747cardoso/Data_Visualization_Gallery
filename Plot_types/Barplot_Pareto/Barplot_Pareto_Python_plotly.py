
# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

# Packages:
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from matplotlib.colors import LinearSegmentedColormap, to_hex
import plotly.graph_objects as go

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

# Cumulative frequency:
df_plot["freq_rel_cum"] = [round(sum(df_plot["freq_rel"].iloc[:(i + 1)]), 3) for i in range(df_plot.shape[0])]
df_plot["freq_rel_cum_char"] = [str(i) + "%" for i in df_plot["freq_rel_cum"]]

# Plot:
n_levels = df_plot.shape[0]
cmap = LinearSegmentedColormap.from_list("my_palette", ["#111539", "#97A1D9"])
my_palette = [to_hex(j) for j in  [cmap(i/n_levels) for i in np.array(range(n_levels))]]

fig = make_subplots(specs = [[{"secondary_y": True}]])
fig.add_trace(
    go.Bar(
        x = df_plot["level"],
        y = df_plot["freq"],
        marker = dict(
            color = [i for i in range(df_plot.shape[0])],
            colorscale = my_palette
        ),
        text = df_plot["freq_rel_char"],
        hovertemplate = "<b>Frequency: %{y:,}</b><extra></extra>"
    ),
    secondary_y = False
)
fig.update_yaxes(type = "log")
fig.update_traces(
    textposition = "outside",
    textfont_color = my_palette[n_levels//2],
    textfont_size = 15
)
fig.add_trace(
    go.Scatter(
        x = df_plot["level"],
        y = df_plot["freq_rel_cum"],
        mode = "lines+markers+text",
        text = df_plot["freq_rel_cum_char"],
        textposition = "bottom center",
        textfont = dict(
            family = "sans serif",
            size = 14,
            color = my_palette[n_levels - 2]
        ),
        hovertemplate = "<b>Cumulative frequency: %{y:,}%</b><extra></extra>"
    ),
    secondary_y = True
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
fig.update_yaxes(
    title_text = "<b>Cumulative frequency</b>", 
    secondary_y = True
)
fig.show()


