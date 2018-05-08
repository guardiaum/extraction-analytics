# set environment
setwd("~/workspace/extraction-analytics/results")

# import packages
library(readr)
library(reshape2)
library(ggplot2)

############################ PLOT GEO PROPS 
# import dataset
geo_props <- read_csv("csv/geo-props-count.csv")
# removes empty columns
geo_props <- geo_props[!sapply(geo_props, function(x) all(is.na(x)))]
# change NA by zero
geo_props[is.na(geo_props)] <- 0
# convert column values to numeric
geo_props[, 2:5] <- sapply(geo_props[, 2:5], as.numeric)
# round column values
geo_props$Latitude <- round(geo_props$Latitude, 3)
geo_props$Longitude <- round(geo_props$Longitude, 3)
geo_props$Coordinates <- round(geo_props$Coordinates, 3)
geo_props$Location <- round(geo_props$Location, 3)
# returns only categories with values not zero
# geo_props <- geo_props[rowSums(geo_props != 0.000) > 1,]
# reshape dataframe
geo_props.m <- melt(geo_props, id.vars = 'Category')
# horizontal bar plot
geoplot <- ggplot(geo_props.m, aes(x=Category, y=value)) + 
  geom_bar(aes(fill=variable), position=position_dodge(width=0.8), stat="identity") + 
  coord_flip() + 
  theme(legend.position=c(0.6,0.43), 
        legend.background=element_rect(fill=alpha('white', 0.8)), 
        legend.title=element_blank(), axis.title.x=element_blank(), axis.title.y=element_blank()) +
  scale_fill_discrete(guide=guide_legend(reverse=T))

ggsave(plot = geoplot, file = '../results/plots/R-geo-props-count.png', device = "png", width = 4.5, height = 5, units = "in", dpi = 600)

############################ PLOT TIME PROPS 
# import dataset
time_props <- read_csv("csv/time-props-count.csv")
# removes empty columns
time_props <- time_props[!sapply(time_props, function(x) all(is.na(x)))]
# change NA by zero
time_props[is.na(time_props)] <- 0
# convert column values to numeric
time_props[, 2:4] <- sapply(time_props[, 2:4], as.numeric)
# round column values
time_props$Date <- round(time_props$Date, 3)
time_props$Period <- round(time_props$Period, 3)
time_props$Time <- round(time_props$Time, 3)
# returns only categories with values not zero
# time_props <- time_props[rowSums(time_props != 0.000) > 1,]
# reshape dataframe
time_props.m <- melt(time_props, id.vars = 'Category')

# horizontal bar plot
timeplot <- ggplot(time_props.m, aes(x=Category, y=value)) + 
  geom_bar(aes(fill=variable), position=position_dodge(width=0.8), stat="identity") + 
  coord_flip() + 
  theme(legend.position=c(0.72,0.5), 
        legend.background=element_rect(fill=alpha('white', 0.8)), legend.title=element_blank(), 
        axis.title.x=element_blank(), axis.title.y=element_blank()) + 
  scale_fill_discrete(guide=guide_legend(reverse=T))
ggsave(plot = timeplot, file = '../results/plots/R-time-props-count.png', device = "png", width = 4.5, height = 5, units = "in", dpi = 600)
