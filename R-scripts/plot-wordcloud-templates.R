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
  filename = paste('plots/template/wordcloud/', unlist(strsplit(f, "\\."))[1], '.png', sep='')

  png(filename, width=12, height=12 ,units="in", res=600)
  cloud <- wordcloud(words = df$Template, freq = df$Count, scale=c(8,.2), min.freq = 0.1,
                      random.order = FALSE, colors=brewer.pal(8, "Dark2"))
  par(mar = rep(0, 4))
  dev.off()
}
