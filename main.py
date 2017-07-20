import my_csv as csv
import statistics as stat
import visualization as v
import pandas as pd

names = []
categories = []
columns = ["Count Articles", "Count Infoboxes", "Count Properties","Avg. Properties"]

# iterates over csv files and calculates infobox statistics
for file in csv.readCSVDirectory("csv/"):
	category = csv.readCSVFile(file)
	categoryName = file.split(".")[0]
	names.append(categoryName)
	# count elements
	articles, infoboxes, props = stat.countElements(category)
	# get properties average
	average = stat.averageInfoboxProperties(category)
	categories.append([articles, infoboxes, props, average])
	# get top 30 properties
	topProperties = stat.topPropertiesByFrequency(category, 30, infoboxes)
	# plot top properties
	v.plotScatter(categoryName, topProperties)
'''
	print("Category: %s" % file);
	print("Articles count: %s" % articles)
	print("Infoboxes count: %s" % infoboxes)
	print("Props count: %s" % props)
	print("Avg. Props: %s" % average)
	print("==========================================")
'''

# saves statistics into csv file
categories = pd.DataFrame(categories, index=names, columns=columns)
categories.to_csv('../results/categories-statistics.csv', index=True, header=True, sep=",")
