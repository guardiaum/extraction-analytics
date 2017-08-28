import util.my_csv as csv
import statistics.common as stat
import statistics.geo_temp as prop
import plotting.visualization as v
import pandas as pd
import clustering.hac_single_linkagematrix as single
import clustering.hac_complete_linkagematrix as complete

'''
	FOR SINGLE EXECUTION
	It is required to inform categoryName
'''

categories = []
columns = ["Count Articles", "Count Infoboxes", "Count Infob. w/ Geoinfo", "Count infob. w/ Datetime","Count Total Properties", "Count Geo Props.", "Count datetime props", "Avg. Properties", "std props", "median props", "var props", "cov props"]

# iterates over csv files and calculates infobox statistics
categoryName = "Geothermal_power_stations"
category = csv.readCSVFile("datasets/"+categoryName+".csv")

print("=================== %s ====================" % categoryName)

# count elements
print("counting elements...")
articles, infoboxes, props = stat.countElements(category)

# geo properties
articlesWithGeoProps = prop.getGeoProps(category)

countArticlesWithGeoProps, countGeoProps = prop.count(articlesWithGeoProps, articles, infoboxes, props)
geoProps = prop.getSortedProperties(articlesWithGeoProps, infoboxes)

v.plotBar(categoryName, geoProps, 'results/plots/geo/', "Geo properties frequency for " + categoryName)

# temporal properties
articlesWithDateTimeProps = prop.getDateTimeProps(category)
countArticlesWithDateTimeProps, countDateTimeProps = prop.count(articlesWithDateTimeProps, articles, infoboxes, props)
dateTimeProps = prop.getSortedProperties(articlesWithDateTimeProps, infoboxes)

v.plotBar(categoryName, dateTimeProps, 'results/plots/datetime/', "DateTime properties frequency for " + categoryName)

# get properties average
print("getting average infobox props...")
average, std, median, variance, covariance = stat.averageInfoboxProperties(category)

categories.append([articles, infoboxes, countArticlesWithGeoProps, countArticlesWithDateTimeProps, props, countGeoProps, countDateTimeProps, average, std, median, variance, covariance])

# get top 30 properties
print("getting top 30 properties...")
topProperties = stat.topPropertiesByProportion(category, 30, infoboxes)

# plot top properties
print("plotting scatter...")
v.plotScatter(categoryName, topProperties, 'results/plots/', "Infobox properties frequency for " + categoryName)
print("------------------------------------------")
print("Category: %s" % categoryName)
print("Articles count: %s" % articles)
print("Total Infoboxes count: %s" % infoboxes)
print("Infoboxes w/ Geo: %s" % countArticlesWithGeoProps)
print("Infoboxes w/ Datetime: %s" % countArticlesWithDateTimeProps)
print("Props count: %s" % props)
print("Geo props count: %s" % countGeoProps)
print("Geo date/time count: %s" % countDateTimeProps)
print("Avg. Props: %s" % average)
print("==========================================")
print("saving statistics to file")

# saves statistics into csv file
categories = pd.DataFrame(categories, index={categoryName}, columns=columns)
path = 'results/csv/%s.csv' % categoryName
categories.to_csv(path, index=True, header=True, sep=",")

clusters, linkagematrix = single.agglomerateAllProperties(category)
print("linkage matrix >> %s" %linkagematrix)
print("FINISHED")
