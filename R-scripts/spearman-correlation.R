# set environment
setwd("~/workspace/extraction-analytics/results")

# import packages
library(readr)

# import dataset 
input <- read_csv("csv/props_usage-template_size-relation.csv")

input$`Props Usage` = as.numeric(as.character(input$`Props Usage`))
input$`Template Size` = as.numeric(as.character(input$`Template Size`))

input = input[order(input$`Props Usage`),]

cor.test( ~ `Props Usage` + `Template Size`,
          data=input, method="spearman",
          continuity=FALSE, conf.level = 0.99)

plot(`Props Usage` ~ `Template Size`, data=input)
