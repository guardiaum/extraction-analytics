# set environment
setwd("~/workspace/extraction-analytics/results")

library(readr)
library(RColorBrewer)
library(wordcloud)
library(ggplot2)

top_props = read_csv("csv/top-props-frequency.csv")

filename = 'plots/wordcloud_props.png'

png(filename, width=6, height=6, units="in", res=600)
cloud <- wordcloud(words = top_props$property, freq = top_props$frequency, 
                   random.order = TRUE, colors=brewer.pal(8, "Dark2"))
dev.off()