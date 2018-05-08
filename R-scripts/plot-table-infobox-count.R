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
colnames(depth_df) <- c("Categories", "Nodes")
depth_df <- depth_df[order(depth_df$Categories),]

# subset infobox counts and category names
infobox_subset = stats[,0:3]
categories_name = infobox_subset[,1]
articles_count = infobox_subset[,2]
infoboxes_count = infobox_subset[,3]
depth_value = depth_df[,2]

descriptions_new = sapply(lapply(stats$description, strwrap, width=90), paste, collapse="\n")

table <- data.frame(Categories = categories_name, Articles = articles_count, Infoboxes = infoboxes_count, Depth = depth_value, Description = descriptions_new)
colnames(table) <- c("Category", "# Articles", "# Infoboxes", "# Nodes", "#Category Description")

columns_alignment <- matrix(c(0, 0.5, 0.5, 0.5, 0), ncol=5, nrow=nrow(table), byrow=TRUE)
x <- matrix(c(0.01, 0.5, 0.5, 0.5, 0.01), ncol=5, nrow=nrow(table), byrow=TRUE)

tt1 <- ttheme_default(base_size=8, core=list(fg_params=list(hjust = as.vector(columns_alignment), 
                                               x = as.vector(x))),
                      colhead=list(fg_params=list(hjust=0, x=0.01)))

#png("plots/R-articles-count.png", height=490, width=320)
grob <- tableGrob(table, rows=NULL, theme=tt1)

# grid.arrange(grob)
# Dimensions: 320x490 (px)
ggsave(plot = grob, 
       file = 'plots/R-articles-count.png', device = "png", width = 10, height = 4, units = "in", dpi = 300)
