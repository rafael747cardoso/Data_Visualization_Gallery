
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(ggplot2, lib = path_lib)

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

df_plot = data.frame(
    "X" = X,
    "Y" = Y,
    "y_fit" = y_fit,
    "y_fit_dw" = y_fit_dw,
    "y_fit_up" = y_fit_up,
)

# Plot:
p = ggplot(
        data = df_plot,
        aes(
            x = X
        )
    ) +
    geom_point(
        aes(
            y = Y,
            color = "point_label"
        ),
        size = 3,
        show.legend = TRUE
    ) +
    geom_ribbon(
        aes(
            ymin = y_fit_dw,
            ymax = y_fit_up,
            fill = "ribbon_label"
        ),
        show.legend = TRUE
    ) +
    geom_line(
        aes(
            y = y_fit,
            color = "line_label"
        ),
        size = 1,
        show.legend = TRUE
    ) +
    scale_fill_manual(
        name = "",
        values = c("ribbon_label" = "#5DDA52"),
        labels = c(paste0(nstd, " sigma confidence interval"))
    ) +
    scale_color_manual(
        name = "",
        values = c("point_label" = "#52A7DA",
                   "line_label" = "#F51616"),
        labels = c("Best fit", "Data")
    ) +
    theme(
        axis.text.x = element_text(
            size = 14,
            angle = 0,
            hjust = 0.5,
            vjust = 1
        ),
        axis.text.y = element_text(
            size = 14
        ),
        axis.title.x = element_text(
            size = 15,
            face = "bold"
        ),
        axis.title.y = element_text(
            size = 15,
            face = "bold"
        ),
        legend.text = element_text(
            size = 14
        ),
        panel.background = element_rect(
            fill = "white"
        ),
        panel.grid.major = element_line(
            size = 0.2,
            linetype = "solid",
            colour = "#eaeaea"
        ),
        panel.grid.minor = element_line(
            size = 0.1,
            linetype = "solid",
            colour = "#eaeaea"
        ),
        plot.margin = margin(
            t = 0, 
            r = 5,
            b = 5, 
            l = 10,
            unit = "pt"
        )
    ) +
    xlab(pred_var_name) +
    ylab(resp_var_name)

p






