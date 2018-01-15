# set environment
setwd("~/workspace/extraction-analytics/results")

library(readr)
library(RColorBrewer)
library(wordcloud)
library(ggplot2)

files = list.files("csv/templates/")

for (f in files)
{
  df = read_csv(paste("csv/templates/", f,  sep=""))
  filename = unlist(strsplit(f, "\\."))[1]
  filename = paste('plots/template/', filename, '.png', sep="")
  png(filename, width=12, height=12, units="in", res=600)
  wordcloud(words = df$Template, freq = df$Count, 
                      random.order = TRUE, colors=brewer.pal(8, "Dark2"))
  dev.off()
}
