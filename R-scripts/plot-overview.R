# set environment
setwd("~/workspace/extraction-analytics/results")

# import packages
library(readr)
library(reshape2)
library(gridExtra)
library(ggplot2)

# Plot for Overview table
# import statistics dataset 
overview <- read_csv("csv/overview.csv")

grob_overview <- tableGrob(overview, cols = c("", "Total"),rows=NULL, theme = ttheme_default(base_size=8))

ggsave(plot = grob_overview, 
       file = 'plots/R-overview-stats.png', device = "png", width = NA, height = NA, units = "in", dpi = 300)

# Plot for histogram of infoboxes count in all categories
cat_inf_counts <- read_csv(file="csv/all-categories-ready.csv", col_names = FALSE)

plot <- ggplot(cat_inf_counts, aes(x=cat_inf_counts$X1)) + 
  xlim(0, 100) +  ylim(0, 220000) + 
  geom_histogram(binwidth=1, colour="black", fill="white") +
  labs(x="Infoboxes count", y="frequency")

ggsave(plot = plot, file="plots/R-infobox-cat-hist.png", device = "png", 
       width = NA, height = NA, units = "in", dpi = 300)

# Plot for template usage table
templates <- read_csv(file="csv/all-categories-template-usage.csv")
grob_templates <- tableGrob(templates, cols = c("", "# Templates", "Most Used", "Freq. (Most Used)"), rows=NULL, theme = ttheme_default(base_size=8))
ggsave(plot = grob_templates, 
       file = 'plots/R-templates-usage.png', device = "png", width = NA, height = NA, units = "in", dpi = 300)

# plot infoboxes types
inf_types <- read_csv("csv/infoboxes_types.csv")

grob_overview <- tableGrob(inf_types, cols = c("Type", "Count Occurences"), rows=NULL, theme = ttheme_default(base_size=8))

ggsave(plot = grob_overview, 
       file = 'plots/R-overview-infoboxes-types.png', device = "png", width = NA, height = NA, units = "in", dpi = 300)

inf_types$Frequency <- prop.table(inf_types$Count)
inf_types$Frequency <- formatC(inf_types$Frequency, format='e', digits = 2)
inf_types <- inf_types[order(-inf_types$Count),]

grob_overview2 <- tableGrob(inf_types[, c("Type", "Frequency")], cols = c("Type", "Frequency"), rows=NULL, theme = ttheme_default(base_size=8))

ggsave(plot = grob_overview2, 
       file = 'plots/R-overview-freq-infoboxes-types.png', device = "png", width = NA, height = NA, units = "in", dpi = 300)


