# set environment
setwd("~/workspace/extraction-analytics/results")

library(readr)
library(RColorBrewer)
library(wordcloud)
library(wordcloud2)
library(ggplot2)

top_props = read_csv("csv/top-props-frequency.csv")

filename = 'plots/wordcloud_top_props.png'

png(filename, width=5, height=5, units="in", res=300)
cloud <- wordcloud(words = top_props$property, freq = top_props$frequency, 
                   random.order = TRUE, colors=brewer.pal(8, "Dark2"))
dev.off()

wordcloud2(data = top_props)
