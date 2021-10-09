
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(plotly, lib = path_lib)

# Dataset:
df = readr::read_csv(paste0(path_data, "nasa_exoplanets.csv")) %>%
         as.data.frame()
attr(df, "spec") = NULL
df_varnames = readr::read_csv(paste0(path_data, "nasa_exoplanets_var_names.csv")) %>%
                  as.data.frame()
attr(df_varnames, "spec") = NULL

# Variables:
resp_var = "pl_orbper"
resp_var_name = (df_varnames %>%
                    dplyr::filter(var == resp_var))$var_name
pred_var = "pl_orbsmax"
pred_var_name = (df_varnames %>%
                    dplyr::filter(var == pred_var))$var_name

# Adapt the data:
df = df %>%
         dplyr::select(all_of(pred_var),
                       all_of(resp_var))
df = df %>% 
         tidyr::drop_na()
df = df %>%
         dplyr::filter(eval(parse(text = resp_var)) < 25000 &
                       eval(parse(text = pred_var)) < 20)

# Fit function:
kepler_orb = function(x, a){
    y = a*x**(1.5)
    return(y)
}

# Regression model:
X = df[, pred_var]
Y = df[, resp_var]
frml = as.formula(paste0(resp_var, "~kepler_orb(", pred_var, ", a)"))
model = nls(formula = frml,
            start = list(a = 1),
            data = df)
popt = as.numeric(model$m$getPars())
pcov = as.numeric(vcov(model))
perr = sqrt(pcov)
nstd = 10
popt_up = popt + nstd*perr
popt_dw = popt - nstd*perr
y_fit = kepler_orb(x = X,
                   a = popt)
y_fit_up = kepler_orb(x = X,
                      a = popt_up)
y_fit_dw = kepler_orb(x = X,
                      a = popt_dw)

# Plot:
p = plot_ly() %>%
    add_trace(
        x = X,
        y = Y,
        type = "scatter",
        mode = "markers",
        marker = list(
            size = 10,
            color = "#52A7DA"
        ),
        hovertemplate = paste0("<b>", pred_var_name, ": %{x} <br> ",
                               resp_var_name, ": %{y} </b><extra></extra>"),
        name = "Data"
    ) %>%
    add_trace(
        x = sort(X),
        y = sort(y_fit_up),
        type = "scatter",
        mode = "lines",
        line = list(
            width = 3,
            color = "#5DDA52"
        ),
        showlegend = FALSE
    ) %>%
    add_trace(
        x = sort(X),
        y = sort(y_fit),
        type = "scatter",
        mode = "lines",
        fill = "tonexty",
        fillcolor = "#5DDA52",
        showlegend = FALSE
    ) %>%
    add_trace(
        x = sort(X),
        y = sort(y_fit),
        type = "scatter",
        mode = "lines",
        line = list(
            width = 3,
            color = "#F51616"
        ),
        name = "Best fit"
    ) %>%
    add_trace(
        x = sort(X),
        y = sort(y_fit_dw),
        type = "scatter",
        mode = "lines",
        line = list(
            width = 3,
            color = "#5DDA52"
        ),
        fill = "tonexty",
        fillcolor = "#5DDA52",
        name = paste0(nstd, " sigma confidence interval")
    ) %>%
    layout(
        xaxis = list(
            title = paste0("<b>", pred_var_name, "</b>"),
            titlefont = list(
                size = 20
            ),
            tickfont = list(
                size = 18
            )
        ),
        yaxis = list(
            title = paste0("<b>", resp_var_name, "</b>"),
            titlefont = list(
                size = 20
            ),
            tickfont = list(
                size = 18
            )
        ),
        margin = list(
            l = 10,
            r = 10,
            t = 10,
            b = 10
        ),
        hoverlabel = list(
            font = list(
                size = 18
            )
        ),
        showlegend = TRUE
    )

p


