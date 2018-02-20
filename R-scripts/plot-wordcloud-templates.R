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
  filename = paste('plots/template/wordcloud/', unlist(strsplit(f, "\\."))[1], sep='')

  png(filename, width=6, height=6, units="in", res=600)
  cloud <- wordcloud(words = df$Template, freq = df$Count, 
                      random.order = TRUE, colors=brewer.pal(8, "Dark2"))
  dev.off()
}
