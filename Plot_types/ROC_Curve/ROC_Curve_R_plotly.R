
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(plotly, lib = path_lib)
require(glmnet, lib = path_lib)
require(glmnet, lib = path_lib)
require(ROCR, lib = path_lib)

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
pred_vars_name = (df_varnames %>%
                     dplyr::filter(var %in% pred_vars))$var_name

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

# ROC curve:
ROCRpred = ROCR::prediction(predictions = probs,
                            labels = df[, eval(resp_var)])
ROCRperf = ROCR::performance(prediction.obj = ROCRpred,
                             measure = "tpr",
                             x.measure = "fpr")
df_plot = data.frame("False_positive_rate" = ROCRperf@x.values[[1]],
                     "True_positive_rate" = ROCRperf@y.values[[1]],
                     "Thresholds" = ROCRperf@alpha.values[[1]]) %>% 
          dplyr::filter(Thresholds >= 0 & 
                        Thresholds <= 1)
preds = ROCR::prediction(predictions = probs, 
                         labels = df[, resp_var])
auc = attr(x = ROCR::performance(prediction.obj = preds,
                                 measure = "auc"), 
           which = "y.values")[[1]]

# Plot:
my_palette = colorRampPalette(c("#111539", "#97A1D9"))

p = plot_ly(
        data = df_plot,
        x = ~False_positive_rate,
        y = ~True_positive_rate,
        color = my_palette(3)[2],
        colors = my_palette(3)[2],
        type = "scatter",
        mode = "lines",
        fill = "tozeroy",
        fillcolor = my_palette(3)[3],
        line = list(
            width = 5
        ),
        hovertemplate = paste0("<b>False positive rate: %{x} <br> ",
                               "True positive rate: %{y} </b><extra></extra>"),
        height = 800,
        width = 800
    ) %>%
    add_trace(
        x = c(0, 1),
        y = c(0, 1),
        type = "scatter",
        mode = "lines",
        line = list(
            width = 2,
            color = "white",
            dash = "dash"
        )
    ) %>%
    layout(
        title = list(
            text = paste0("AUC = ", round(auc, digits = 3)),
            titlefont = list(size = 20),
            tickfont = list(size = 18)
        ),
        xaxis = list(
            title = paste0("<b>False positive rate</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18),
            categoryorder = "array"
        ),
        yaxis = list(
            title = paste0("<b>True positive rate</b>"),
            titlefont = list(size = 20),
            tickfont = list(size = 18)
        ),
        margin = list(
            l = 10,
            r = 10,
            t = 50,
            b = 10
        ),
        hoverlabel = list(font = list(size = 18)),
        showlegend = FALSE
    )

p









