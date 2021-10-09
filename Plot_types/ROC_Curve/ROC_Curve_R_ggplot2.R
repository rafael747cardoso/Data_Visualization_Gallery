
# Paths:
path_data = "data/"
path_lib = "renv/library/R-4.1/x86_64-pc-linux-gnu/"

# Packages:
require(dplyr, lib = path_lib)
require(tidyr, lib = path_lib)
require(maditr, lib = path_lib)
require(readr, lib = path_lib)
require(RColorBrewer, lib = path_lib)
require(ggplot2, lib = path_lib)
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

p = ggplot(
        data = df_plot,
        aes(
            x = False_positive_rate,
            y = True_positive_rate
        )
    ) +
    geom_line(
        show.legend = FALSE,
        color = my_palette(3)[2],
        size = 2
    ) +
    geom_area(
        position = "identity",
        fill = my_palette(3)[3]
    ) +
    geom_abline(
        intercept = 0,
        slope = 1,
        linetype = "dashed",
        show.legend = FALSE,
        color = "white",
        size = 1.1,
        alpha = 0.6
    ) +
    coord_fixed(ratio = 1) + 
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
    xlab("False positive rate") +
    ylab("True positive rate") +
    ggtitle(paste0("AUC = ", round(auc, digits = 3)))

p


