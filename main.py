import my_csv as csv
import statistics as stat
import visualization as v
import pandas as pd

names = []
categories = []
columns = ["Count Articles", "Count Infoboxes", "Count Properties","Avg. Props", "std props", "median props"]
path_to_plots = '../results/plots/'

# iterates over csv files and calculates infobox statistics
for file in csv.readCSVDirectory("datasets/"):
	category = csv.readCSVFile(file)
	categoryName = file.split(".")[0]
	names.append(categoryName)
	print("=================== %s ====================" % categoryName)
	# count elements
	print("counting elements...")
	articles, infoboxes, props = stat.countElements(category)
	# get properties average
	print("getting average infobox props...")
	average, std, median = stat.averageInfoboxProperties(category)
	categories.append([articles, infoboxes, props, average, std, median])
	# get top 30 properties
	print("getting top 30 properties...")
	topProperties = stat.topPropertiesByFrequency(category, 30, infoboxes)
	# plot top properties
	print("plotting scatter...")
	v.plotScatter(categoryName, topProperties, path_to_plots)
	print("------------------------------------------")
	print("Category: %s" % file);
	print("Articles count: %s" % articles)
	print("Infoboxes count: %s" % infoboxes)
	print("Props count: %s" % props)
	print("Avg. Props: %s" % average)
	print("==========================================")

print("saving statistics to file")
# saves statistics into csv file
categories = pd.DataFrame(categories, index=names, columns=columns)
categories.to_csv('../results/csv/categories-statistics.csv', index=True, header=True, sep=",")
print("FINISHED")
