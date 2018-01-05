# set environment
setwd("~/workspace/extraction-analytics/results")

# import packages
library(readr)
library(reshape2)
library(gridExtra)
library(ggplot2)

# import statistics dataset 
stats <- read_csv("csv/general-statistics.csv")
stats <- stats[order(stats$X1),]

depth_df <- read_csv("csv/categories-depth.csv", col_names=FALSE)
colnames(depth_df) <- c("Categories", "Depth")
depth_df <- depth_df[order(depth_df$Categories),]

# subset infobox counts and category names
infobox_subset = stats[,0:2]
categories_name = infobox_subset[,1]
articles_count = infobox_subset[,2]
depth_value = depth_df[,2]

table <- data.frame(Categories = categories_name, Articles = articles_count, Depth = depth_value)
colnames(table) <- c("Categories", "Articles Count", "Depth")

#png("plots/R-articles-count.png", height=490, width=320)
grob <- tableGrob(table, rows=NULL, theme = ttheme_default(base_size=8))

# grid.arrange(grob)
# Dimensions: 320x490 (px)
ggsave(plot = grob, 
       file = 'plots/R-articles-count.png', device = "png", 
       width = 3.30, height = 5, units = "in", dpi = 300)
