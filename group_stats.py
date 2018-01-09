import util.my_csv as csv
import util.constants as constants
import statistics.common as stat
import statistics.geo_temp as prop
import plotting.visualization as v
import pandas as pd
import util.input as inp

'''
    STATISTIC EXECUTION
    FOR GROUP OF CATEGORIES
    It is required to inform categoriesName, 
    output file name, title for plot and subtitle if needed
'''

# CSV columns for statistics result file
columns = ["Count Articles", "Count Infoboxes", "Count Infob. w/ Geoinfo",
           "Count infob. w/ Datetime","Count Total Properties", "Avg. Properties",
           "std props", "median props", "Infobox props miss usage index"]

# CSV columns for bigger infoboxes
biggerInfoboxesColumns = ["Article", "Size", "Properties"]

# Read datasets
categoriesName = inp.readFiles(constants.infobox_datasets)

names = []
categoriesResult = []
biggerInfoboxes = []
infoboxesSizeByCategory = []

# Iterates over csv files and calculates infobox statistics
for categoryName in categoriesName:
    category = csv.readCSVFile(constants.infobox_datasets+"/"+categoryName)
    categoryName = categoryName.replace(".csv","")
    names.append(categoryName)
    print("=================== %s ====================" % categoryName)

    # Big Infobox
    bigInfobox_name, bigInfobox_properties = stat.getBiggerInfobox(category)
    biggerInfoboxes.append([bigInfobox_name, bigInfobox_properties.shape[0], bigInfobox_properties.flatten()])

    # count elements
    print("counting elements...")
    articles_count, infoboxes_count, common_props_count = stat.countElements(category)

    # count articles with geo and datetime properties
    # geo
    articlesWithGeoProps = prop.getGeoProps(category)
    countArticlesWithGeoProps, countGeoProps = articlesWithGeoProps.shape
    # datetime
    articlesWithDateTimeProps = prop.getDateTimeProps(category)
    countArticlesWithDateTimeProps, countDateTimeProps = articlesWithDateTimeProps.shape

    # get properties average
    average, std, median = stat.averageInfoboxProperties(category)

    # calculates infobox properties miss usage
    propertiesProportion = stat.propertiesProportion(category, infoboxes_count)
    props_missing_usage = stat.getMissingUsage(propertiesProportion)

    # append to create csv file
    categoriesResult.append([articles_count, infoboxes_count, countArticlesWithGeoProps,
                             countArticlesWithDateTimeProps, common_props_count, average,
                             std, median, props_missing_usage])

    # Plot infoboxes size distribution per category
    propertiesDistribution = stat.getInfoboxesDistribution(category)
    infoboxesSizeByCategory.append(propertiesDistribution.values)
    v.plotInfoboxesDistribution(categoryName, propertiesDistribution, 'results/plots/distr')

    # get top 30 properties
    print("getting top 30 properties...")
    topProperties = stat.topPropertiesByProportion(category, 30, infoboxes_count)
    v.plotScatter(categoryName, topProperties, 'results/plots/scatter/', "Properties proportion: " + categoryName)

    print("------------------------------------------")
    print("Category: %s" % categoryName)
    print("Articles count: %s" % articles_count)
    print("Total Infoboxes count: %s" % infoboxes_count)
    print("Infoboxes w/ Geo: %s" % countArticlesWithGeoProps)
    print("Infoboxes w/ Datetime: %s" % countArticlesWithDateTimeProps)
    print("Common props count: %s" % common_props_count)
    print("Geographic props count: %s" % countGeoProps)
    print("DateTime props count: %s" % countDateTimeProps)
    print("Avg. Props: %s" % average)
    print("Props miss usage: %s" % props_missing_usage)
    print("==========================================")

print("saving statistics to file")

# boxplot of infoboxes size by category
v.plotInfoboxesSizeBoxplot(names, infoboxesSizeByCategory, "results/plots/distr/infoboxes-size-all.png")

# saves statistics into csv file
categoriesResult = pd.DataFrame(categoriesResult, index=names, columns=columns)
path = 'results/csv/general-statistics.csv'
categoriesResult.to_csv(path, index=True, header=True, sep=",")

# saves bigger infoboxes
biggerInfoboxes = pd.DataFrame(biggerInfoboxes, index=names, columns=biggerInfoboxesColumns)
pathBigInfoboxes = 'results/csv/big-infoboxes.csv'
biggerInfoboxes.to_csv(pathBigInfoboxes, index=True, header=True, sep=",")

print("FINISHED")
