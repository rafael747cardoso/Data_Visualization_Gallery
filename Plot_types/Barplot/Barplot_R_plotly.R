
# Packages:
require(plotly)
require(dplyr)
require(RColorBrewer)

# Paths:
path_data = "data/"
path_plot = "Plot_types/Barplot/"

# Dataset:
df = read.csv(paste0(path_data, "nasa_exoplanets.csv"),
              sep = ",")
df_varnames = read.csv(paste0(path_data, "nasa_exoplanets_var_names.csv"),
                       sep = ";")

# Variables:
cat_var = "discoverymethod"
cat_var_name = (df_varnames %>%
                    dplyr::filter(var == cat_var))$var_name

# Adapt the data:
df_plot = df %>%
    dplyr::group_by(eval(parse(text = cat_var))) %>%
    dplyr::summarise(freq = n()) %>%
    as.data.frame() %>%
    dplyr::arrange(desc(freq))
names(df_plot)[1] = "level"

# Deal with NA:
na_separeted = TRUE
if(na_separeted){
    df_plot$level[which(df_plot$level == "")] = NA
} else{
    df_plot$level[which(df_plot$level == "")] = "NA"
}

# Levels order:
df_plot$level = factor(x = df_plot$level,
                       levels = unique(df_plot$level))
df_plot$freq_rel = paste0(round(df_plot$freq/sum(df_plot$freq)*100,
                                digits = 3), "%")

# Plot:
my_colors = colorRampPalette(list('yellow', 'red'))(15)

plot_ly(
    data = df_plot,
    x = ~level,
    y = ~freq,
    type = "bar"#,
    # text = ~freq_rel,
    # texttemplate = "%{text}",
    # textposition = "outside",
    # marker = list(color = my_colors)
    # color = ~level
    # cols = colorRampPalette(c("blue", "red"))(nrow(df_plot))
) %>%
    layout(
        xaxis = list(
            title = cat_var_name,
            tickfont = list(size = 15),
            titlefont = list(size = 20)
        ),
        yaxis = list(
            title = "Frequency",
            tickfont = list(size = 15),
            titlefont = list(size = 20),
            type = "log"
        ),
        margin = list(
            l = 5,
            r = 5,
            t = 5,
            b = 5
        )
    )


