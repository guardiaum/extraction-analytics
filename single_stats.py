import my_csv as csv
import statistics as stat
import visualization as v
import pandas as pd

categories = []
columns = ["Count Articles", "Count Infoboxes", "Count Properties","Avg. Properties"]

# iterates over csv files and calculates infobox statistics
categoryName = "Protein_domains"
category = csv.readCSVFile("csv/"+categoryName+".csv")

print("=================== %s ====================" % categoryName)

# count elements
print("counting elements...")
articles, infoboxes, props = stat.countElements(category)

# get properties average
print("getting average infobox props...")
average = stat.averageInfoboxProperties(category)

categories.append([articles, infoboxes, props, average])

# get top 30 properties
print("getting top 30 properties...")
topProperties = stat.topPropertiesByFrequency(category, 30, infoboxes)

# plot top properties
print("plotting scatter...")
v.plotScatter(categoryName, topProperties, 'results/plots/')
print("------------------------------------------")
print("Category: %s" % categoryName);
print("Articles count: %s" % articles)
print("Infoboxes count: %s" % infoboxes)
print("Props count: %s" % props)
print("Avg. Props: %s" % average)
print("==========================================")

print("saving statistics to file")
# saves statistics into csv file
categories = pd.DataFrame(categories, columns=columns)
path = 'results/csv/%s.csv' % categoryName
categories.to_csv(path, index=True, header=True, sep=",")

print("FINISHED")
