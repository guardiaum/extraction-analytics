import util.my_csv as csv
import statistics.common as stat
import statistics.geo_temp as prop
import plotting.visualization as v
import pandas as pd
import util.input as inp

'''
	FOR SINGLE EXECUTION
	It is required to inform categoryName
'''

# CSV columns for statistics result file
columns = ["Count Articles", "Count Infoboxes", "Count Infob. w/ Geoinfo", "Count infob. w/ Datetime","Count Total Properties", "Count Geo Props.", "Count datetime props", "Avg. Properties", "std props", "median props", "var props", "cov props"]

# Lines from result file CSV
categories = []

# iterates over csv files and calculates infobox statistics
categoryName = inp.readFile() # Read datasets name
categoryName = categoryName.replace(".csv","")

category = csv.readCSVFile("datasets/"+categoryName+".csv")

print("=================== %s ====================" % categoryName)

# Big Infobox
bigInfobox_name, bigInfobox_properties = stat.getBiggerInfobox(category)

# count elements
print("counting elements...")
articles, infoboxes, props = stat.countElements(category)

# geo properties
articlesWithGeoProps = prop.getGeoProps(category)
countArticlesWithGeoProps = 0
countGeoProps = 0
if(articlesWithGeoProps.size!=0):
	#countArticlesWithGeoProps, countGeoProps = prop.count(articlesWithGeoProps, articles, infoboxes, props)
	geoProps = prop.countGeographicProps(category) #prop.getSortedProperties(articlesWithGeoProps, infoboxes)
	v.plotBar(categoryName, geoProps, 'results/plots/geo/', "Geographic propert. proportion for " + categoryName)

# temporal properties
articlesWithDateTimeProps = prop.getDateTimeProps(category)
countArticlesWithDateTimeProps = 0
countDateTimeProps = 0
if(articlesWithDateTimeProps.size!=0):
	#countArticlesWithDateTimeProps, countDateTimeProps = prop.count(articlesWithDateTimeProps, articles, infoboxes, props)
	dateTimeProps = prop.countDateTimeProps(category) #prop.getSortedProperties(articlesWithDateTimeProps, infoboxes)
	v.plotBar(categoryName, dateTimeProps, 'results/plots/datetime/', "DateTime proportion for " + categoryName)

# get properties average
print("getting average infobox props...")
average, std, median, variance, covariance = stat.averageInfoboxProperties(category)

categories.append([articles, infoboxes, countArticlesWithGeoProps, countArticlesWithDateTimeProps, props, countGeoProps, countDateTimeProps, average, std, median, variance, covariance])

# get top 30 properties
print("getting top 30 properties...")
topProperties = stat.topPropertiesByProportion(category, 30, infoboxes)

# Plot properties distribution per category
infoboxesDistribution = stat.getInfoboxesDistribution(category, topProperties)
v.plotInfoboxesDistribution(categoryName, infoboxesDistribution, 'results/plots/distr/', "Properties distribution per category")

# plot top properties
print("plotting scatter...")
v.plotScatter(categoryName, topProperties, 'results/plots/scatter/', "Properties proportion for " + categoryName)

print("------------------------------------------")
print("Category: %s" % categoryName)
print("Articles count: %s" % articles)
print("Total Infoboxes count: %s" % infoboxes)
print("Infoboxes w/ Geo: %s" % countArticlesWithGeoProps)
print("Infoboxes w/ Datetime: %s" % countArticlesWithDateTimeProps)
print("Common props count: %s" % props)
print("Geo props count: %s" % countGeoProps)
print("Geo date/time count: %s" % countDateTimeProps)
print("Avg. Props: %s" % average)
print("==========================================")
print("saving statistics to file")

# saves statistics into csv file
categories = pd.DataFrame(categories, index={categoryName}, columns=columns)
path = 'results/csv/%s.csv' % categoryName
categories.to_csv(path, index=True, header=True, sep=",")

print("FINISHED")
