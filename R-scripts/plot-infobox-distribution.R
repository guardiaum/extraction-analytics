# set environment
setwd("~/workspace/extraction-analytics/results")

# import packages
library(readr)
library(reshape2)
library(ggplot2)

# import statistics dataset 
all <- read_csv("csv/general-statistics.csv")

# subset infobox counts and category names
infobox_subset = all[,0:5]
categories = infobox_subset[,1]
articles = infobox_subset[,2]
infoboxes = infobox_subset[,3]
geoinfo = infobox_subset[,4]
datetime = infobox_subset[,5]

# create dataframe with statistical subsets
df <- data.frame(Categories = categories, Articles = articles, Infoboxes = infoboxes, Geoinfo = geoinfo, Datetime = datetime)
colnames(df) <- c("Categories", "Articles", "Infoboxes", "GeoInfo", "Datetime")

df$Infoboxes = df$Infoboxes / df$Articles
df$GeoInfo = df$GeoInfo / df$Articles
df$Datetime = df$Datetime / df$Articles

df <- df[ , c("Categories","Infoboxes","GeoInfo", "Datetime")]

# melt dataframe for plotting
df.m <- melt(df, id.vars='Categories')

# plot infos
plot <- ggplot(df.m, aes(x=Categories, y=value)) + 
  geom_bar(aes(fill = variable), width=1.0, position = position_dodge(width=0.8), stat="identity") + 
  coord_flip() + theme(legend.position=c(0.75,0.2), legend.background=element_rect(fill=alpha('white', 0.7)),
                       legend.title = element_blank(), axis.title.x=element_blank(), axis.title.y=element_blank()) +
                       scale_fill_discrete(guide=guide_legend(reverse=T))
                    
ggsave(plot = plot, file = 'plots/R-infobox-proportion.png', device = "png", width = 4.5, height = 5, units = "in", dpi = 600)



