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

categories_name <- stats[,1]
miss_usage <- stats[,ncol(stats)]

table <- data.frame(Categories = categories_name, Miss = miss_usage)
colnames(table) <- c("Category", "Miss usage index")

grob <- tableGrob(table, rows=NULL, theme = ttheme_default(base_size=8))

# Dimensions: 320x490 (px)
ggsave(plot = grob, 
       file = 'plots/R-miss-usage-index.png', device = "png", 
       width = NA, height = NA, units = "in", dpi = 300)
