# set environment
setwd("~/workspace/extraction-analytics/results")

# import packages
library(readr)
library(reshape2)
library(gridExtra)
library(ggplot2)

# Plot for Overview table
# import statistics dataset 
overview <- read_csv("csv/overview.csv", col_names = c("Component", "Total"))

grob_overview <- tableGrob(overview, cols = c("", "Total"),rows=NULL, theme = ttheme_default(base_size=8))

ggsave(plot = grob_overview, 
       file = 'plots/R-overview-stats.png', device = "png", width = NA, height = NA, units = "in", dpi = 300)

# Plot for histogram of infoboxes count in all categories
cat_inf_counts <- read_csv(file="csv/all-categories-ready.csv", col_names = FALSE)

plot <- ggplot(cat_inf_counts, aes(x=cat_inf_counts$X1)) + 
  xlim(0, 100) +  ylim(0, 225000) + 
  theme(text = element_text(size=16), axis.text.x = element_text(size=16), axis.text.y = element_text(size=16)) +
  geom_histogram(binwidth=1, colour="black", fill="white") +
  labs(x="Infoboxes count", y="Frequency")

ggsave(plot = plot, file="plots/R-infobox-cat-hist.png", device = "png", 
       width = NA, height = NA, units = "in", dpi =200)

# Plot for template usage table
templates <- read_csv(file="csv/all-categories-template-usage.csv")
grob_templates <- tableGrob(templates, cols = c("Category", "# Templates", "Most Used", "Size (Most Used)", "Freq. (Most Used)"), rows=NULL, theme = ttheme_default(base_size=8))
ggsave(plot = grob_templates, 
       file = 'plots/R-templates-usage.png', device = "png", width = NA, height = NA, units = "in", dpi = 300)

# plot top most used templates
top_templates <- read_csv(file="csv/top-templates-frequency.csv")
top_templates$proportion = formatC(top_templates$proportion, format = 'e', digits = 2)
grob_top_templates <- tableGrob(top_templates[0:10,], cols=c("Template", "Proportion"), rows=NULL, theme = ttheme_default(base_size=8))
ggsave(plot = grob_top_templates, 
       file = 'plots/R-top-templates-by-proportion.png', device='png',  
       width = NA, height = NA, units = "in", dpi = 300)

# plot infoboxes types
inf_types <- read_csv("csv/infoboxes_types_count.csv", col_names = c("Mapping", "Count"))

inf_types$Frequency <- prop.table(inf_types$Count)
inf_types$Frequency <- formatC(inf_types$Frequency, format='e', digits = 2)
inf_types <- inf_types[order(-inf_types$Count),]

grob_overview2 <- tableGrob(inf_types[, c("Mapping", "Frequency")], cols = c("Mapping", "Frequency"), rows=NULL, theme = ttheme_default(base_size=8))

ggsave(plot = grob_overview2, 
       file = 'plots/R-overview-freq-infoboxes-types.png', device = "png", width = NA, height = NA, units = "in", dpi = 300)

# plot big infoboxes by category
big_infoboxes <- read_csv("csv/big-infoboxes.csv")
grob_big_infoboxes <- tableGrob(big_infoboxes[,c("Category", "Bigger Infobox", "Size")], rows=NULL, theme = ttheme_default(base_size=8))
ggsave(plot=grob_big_infoboxes, file='plots/R-big-infoboxes.png', device='png', width=NA, height=NA, units='in', dpi=300)
