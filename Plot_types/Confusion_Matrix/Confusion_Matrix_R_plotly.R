
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(plotly, lib = path_lib)
require(glmnet, lib = path_lib)
require(caret, lib = path_lib)

# Dataset:
df = readr::read_csv(paste0(path_data, "nasa_exoplanets.csv")) %>%
         as.data.frame()
attr(df, "spec") = NULL
df_varnames = readr::read_csv(paste0(path_data, "nasa_exoplanets_var_names.csv")) %>%
                  as.data.frame()
attr(df_varnames, "spec") = NULL

# Variables:
resp_var = "ttv_flag"
resp_var_name = (df_varnames %>%
                    dplyr::filter(var == resp_var))$var_name
pred_vars = c("sy_snum", "sy_pnum", "disc_year", "pl_orbeccen", "st_teff", "st_mass", "sy_pm",
              "sy_dist", "sy_gaiamag")
pred_vars_names = c()
for(i in 1:length(pred_vars)){
    pred_vars_names = c(pred_vars_names,
                      df_varnames$var_name[which(df_varnames$var == pred_vars[i])])
}

# Adapt the data:
df = df %>%
         dplyr::select(all_of(resp_var), 
                       all_of(pred_vars))
df = df %>% 
         tidyr::drop_na()

# Classification model:
X = df %>% 
        dplyr::select(all_of(pred_vars)) %>%
        as.matrix()
Y = df %>% 
        transmute(y = as.numeric(eval(parse(text = resp_var)))) %>%
        as.matrix()
fit = glmnet(x = X,
             y = Y,
             family = "binomial",
             standardize = TRUE)
cv.fit = cv.glmnet(x = X,
                   y = Y,
                   family = "binomial")
min_lambda = cv.fit$lambda.min
coefs = coef(object = fit, 
             s = min_lambda)
probs = predict(object = fit,
                newx = X,
                type = "response",
                s = min_lambda) %>%
            as.numeric()

# Confusion matrix:
pred = ifelse(probs > 0.5, 1, 0) %>%
           as.factor()
actl = (df %>%
            dplyr::select(all_of(resp_var)))[, 1] %>%
           as.factor()
cm = caret::confusionMatrix(data = pred,
                            reference = actl,
                            dnn = c("Predicted", "Actual"))
df_plot = as.data.frame(cm$table)
x_vals = attr(x = cm$table, which = "dimnames")$Predicted
y_vals = attr(x = cm$table, which = "dimnames")$Actual

# Plot:
my_palette = c("#540A5C", "#E008F8", "#F81D08", "#F88A08")

p = plot_ly(
    data = df_plot,
    x = ~Predicted,
    y = ~Actual,
    z = ~Freq,
    type = "heatmap",
    colors = my_palette,
    colorbar = list(
        title = paste0("<b>Counts</b>"),
        len = 1
    ),
    hoverinfo = "none"
)
x_ind = 1
for(x_val in x_vals){
    y_ind = 1
    for(y_val in y_vals){
        p = p %>%
            add_annotations(
                x = x_val,
                y = y_val,
                text = cm$table[x_ind, y_ind],
                xref = "x",
                yref = "y",
                showarrow = FALSE,
                font = list(
                    color = "white",
                    size = 30
                )
            )
        y_ind = y_ind + 1
    }
    x_ind = x_ind + 1
}
p = p %>%
    layout(
        height = 800,
        width = 800,
        xaxis = list(
            title = paste0("<b>Predicted</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18),
            categoryorder = "array"
        ),
        yaxis = list(
            title = paste0("<b>Actual</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18)
        ),
        margin = list(
            l = 10,
            r = 10,
            t = 10,
            b = 10
        ),
        hoverlabel = list(font = list(size = 18))
    )

p




