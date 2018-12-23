# set environment
#setwd("~/workspace/extraction-analytics/results")

library(readr)
library(RColorBrewer)
library(wordcloud)
library(wordcloud2)
library(ggplot2)

top_props = read_csv("csv/top-props.csv")

filename = 'plots/wordcloud_top_props.png'

png(filename, width=5, height=5, units="in", res=200)
cloud <- wordcloud(words = top_props$property, freq = top_props$proportion, 
                   max.words = 100, random.order = FALSE, 
                   colors=brewer.pal(8, "Dark2"), rot.per = 0.6)
dev.off()

colors = rep(brewer.pal(8, "Dark2"), length.out=nrow(top_props))

wordcloud2(data = top_props, rotateRatio = 0.25, 
           shape = 'circle', minRotation = 1.57, 
           maxRotation = 1.57, size=0.8, max, color = colors)

