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
           "std props", "median props", "var props", "cov props"]

# CSV columns for bigger infoboxes
biggerInfoboxesColumns = ["Article", "Size", "Properties"]

# Read datasets
categoriesName = inp.readFiles(constants.infobox_datasets)

names = []
categoriesResult = []
biggerInfoboxes = []

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
    articles, infoboxes, props = stat.countElements(category)

    # count articles with geo and datetime properties
    # geo
    articlesWithGeoProps = prop.getGeoProps(category)
    countArticlesWithGeoProps, countGeoProps = articlesWithGeoProps.shape
    # datetime
    articlesWithDateTimeProps = prop.getDateTimeProps(category)
    countArticlesWithDateTimeProps, countDateTimeProps = articlesWithDateTimeProps.shape

    # get properties average
    average, std, median, variance, covariance = stat.averageInfoboxProperties(category)

    categoriesResult.append([articles, infoboxes, countArticlesWithGeoProps,
                             countArticlesWithDateTimeProps, props, average,
                             std, median, variance, covariance])


    # Plot properties distribution per category
    infoboxesDistribution = stat.getInfoboxesDistribution(category)
    v.plotInfoboxesDistribution(categoryName, infoboxesDistribution,
                                'results/plots/distr/', "Infobox size distribution: " + categoryName)

    # get top 30 properties
    print("getting top 30 properties...")
    topProperties = stat.topPropertiesByProportion(category, 30, infoboxes)
    v.plotScatter(categoryName, topProperties, 'results/plots/scatter/', "Properties proportion: " + categoryName)

    print("------------------------------------------")
    print("Category: %s" % categoryName)
    print("Articles count: %s" % articles)
    print("Total Infoboxes count: %s" % infoboxes)
    print("Infoboxes w/ Geo: %s" % countArticlesWithGeoProps)
    print("Infoboxes w/ Datetime: %s" % countArticlesWithDateTimeProps)
    print("Common props count: %s" % props)
    print("Geographic props count: %s" % countGeoProps)
    print("DateTime props count: %s" % countDateTimeProps)
    print("Avg. Props: %s" % average)
    print("==========================================")

print("saving statistics to file")

# saves statistics into csv file
categoriesResult = pd.DataFrame(categoriesResult, index=names, columns=columns)
path = 'results/csv/generalStatistics.csv'
categoriesResult.to_csv(path, index=True, header=True, sep=",")

# saves bigger infoboxes
biggerInfoboxes = pd.DataFrame(biggerInfoboxes, index=names, columns=biggerInfoboxesColumns)
pathBigInfoboxes = 'results/csv/big-infoboxes.csv'
biggerInfoboxes.to_csv(pathBigInfoboxes, index=True, header=True, sep=",")

print("FINISHED")
