
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
df_plot = df %>%
              dplyr::select(all_of(resp_var), 
                            all_of(pred_vars))
df_plot = df_plot %>% 
              tidyr::drop_na()

# Classification model:
X = df_plot %>% 
        dplyr::select(all_of(pred_vars)) %>%
        as.matrix()
Y = df_plot %>% 
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
                s = min_lambda)

# Confusion matrix:
pred = ifelse(probs > 0.5, 1, 0)
confusion_matrix = table(pred[, 1], 
                         "data" = (df_plot %>%
                                      dplyr::select(all_of(resp_var)))[, 1])
# x_vals = attr(x = confusion_matrix, which = "dimnames")[[1]]
# y_vals = attr(x = confusion_matrix, which = "dimnames")[[2]]
confusion_matrix = matrix(data = c(as.integer(names(confusion_matrix)), confusion_matrix),
                          nrow = 2,
                          ncol = 2,
                          dimnames = list(x_vals, y_vals)) %>%
                       as.data.frame()
confusion_matrix = confusion_matrix %>%
                       as.data.frame()

# Plot:
my_colors = c("#540A5C", "#E008F8", "#F81D08", "#F88A08")
my_palette = colorRampPalette(colors = my_colors)

p = ggplot(
    data = confusion_matrix,
        aes(
            x = data,
            y = Var1,
            fill = Freq
        )
    ) +
    geom_tile() +
    coord_fixed(
        ratio = 1
    ) +
    scale_fill_gradientn(
        colors = my_palette(100),
        na.value = "white"
    ) +
    geom_text(
        aes(
            x = data, 
            y = Var1, 
            label = Freq
        ),
        color = "white",
        size = 7
    ) +
    theme(
        axis.text.x = element_text(
            size = 14,
            angle = 0,
            hjust = 1,
            vjust = 1
        ),
        axis.text.y = element_text(size = 14),
        axis.title.x = element_text(
            size = 15,
            face = "bold"
        ),
        axis.title.y = element_text(
            size = 15,
            face = "bold"
        ),
        panel.background = element_rect(fill = "white"),
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
    labs(
        x = "Predicted",
        y = "Actual",
        fill = paste0("Counts")
    )

p


