# set environment
setwd("~/workspace/extraction-analytics/results")

# import packages
library(readr)
library(reshape2)
library(ggplot2)

############################ PLOT GEO PROPS 
# import dataset
geo_props <- read_csv("csv/geo/geo-props-count.csv")
# removes empty columns
geo_props <- geo_props[!sapply(geo_props, function(x) all(is.na(x)))]
# reshape dataframe
geo_props.m <- melt(geo_props, id.vars = 'Category')
# change na by zero
geo_props.m[is.na(geo_props.m)] <- 0
# convert column value to numeric
geo_props.m$value <- sapply(geo_props.m[,'value'], as.numeric)
# round column value to 4 decimals
geo_props.m$value <- round(geo_props.m$value, 4)
# horizontal bar plot
png(filename = 'csv/geo/geo-props-count.png', width = 420, height = 400, units = "px")
ggplot(geo_props.m, aes(x=Category, y=value)) + geom_bar(aes(fill=variable), width=1.0, position=position_dodge(width=0.8), stat="identity") + coord_cartesian(xlim = c(0.0, 1.0)) + coord_flip() + theme(axis.text.x = element_text(angle=90, hjust=1), legend.position=c(0.7,0.2), legend.background=element_rect(fill=alpha('white', 0.8)), legend.title=element_blank(), axis.title.x=element_blank(), axis.title.y=element_blank())
dev.off()

############################ PLOT TIME PROPS 
# import dataset
time_props <- read_csv("csv/time/time-props-count.csv")
# removes empty columns
time_props <- time_props[!sapply(time_props, function(x) all(is.na(x)))]
# reshape dataframe
time_props.m <- melt(time_props, id.vars = 'Category')
# change na by zero
time_props.m[is.na(time_props.m)] <- 0
# convert column value to numeric
time_props.m$value <- sapply(time_props.m[,'value'], as.numeric)
# round column value to 4 decimals
time_props.m$value <- round(time_props.m$value, 4)
# horizontal bar plot
png(filename = 'csv/time/time-props-count.png', width = 420, height = 400, units = "px")
ggplot(time_props.m, aes(x=Category, y=value)) + geom_bar(aes(fill=variable), width=1.0, position=position_dodge(width=0.8), stat="identity") + coord_cartesian(xlim = c(0.0, 1.0)) + coord_flip() + theme(axis.text.x = element_text(angle=90, hjust=1), legend.position=c(0.7,0.2), legend.background=element_rect(fill=alpha('white', 0.8)), legend.title=element_blank(), axis.title.x=element_blank(), axis.title.y=element_blank())
dev.off()
