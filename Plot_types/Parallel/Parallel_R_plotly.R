
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
my_vars = c("discoverymethod", "pl_orbper", "st_teff", "disc_locale", "sy_gaiamag")
my_vars_names = c()
for(i in 1:length(my_vars)){
    my_vars_names = c(my_vars_names,
                      df_varnames$var_name[which(df_varnames$var == my_vars[i])])
}

# Adapt the data:
df_plot = df %>%
              dplyr::filter(pl_letter == "d")
df_plot = df_plot[, my_vars]
df_plot = df_plot %>% 
              tidyr::drop_na()

# Plot:
vars_plots = list()
for(i in 1:length(my_vars)){
    var = my_vars[i]
    if(!(class(df_plot[, var]) %in% c("numeric", "float"))){
        # Categorical variables:
        vals_unique = sort(unique(df_plot[, var]))
        df_var = data.frame(
            level_val = vals_unique,
            level_num = 1:length(vals_unique),
            stringsAsFactors = FALSE
        )
        vars_plots[[i]] = list(
            tickvals = df_var$level_num,
            ticktext = vals_unique,
            label = my_vars_names[i],
            values = (df_plot %>%
                         dplyr::left_join(df_var,
                                          by = structure(names = var,
                                                         .Data = "level_val")))$level_num
        )
    } else{
        # Numerical variables:
        var_vals = df_plot[, var]
        vars_plots[[i]] = list(
            range = c(min(var_vals), max(var_vals)),
            label = my_vars_names[i],
            values = var_vals
        )
    }
    vars_plots
}


p = plot_ly(
    dimensions = vars_plots,
    type = "parcoords"
) %>%
    layout(
        font = list(
            size = 18
        ),
        margin = list(
            l = 230,
            r = 60,
            t = 10,
            b = 50
        )
    )

p



