import util.my_csv as my_csv
import util.constants as constants
import statistics.common as stat
import statistics.geo_temp as prop
import plotting.visualization as v
import pandas as pd
import util.input as inp
import numpy as np
import csv

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

def saveBigInfoboxesInfo(categoryName, category, namesLength):
    print("saving big infoboxes to file")
    bigInfobox_name, bigInfobox_properties = stat.getBiggerInfobox(category)

    biggerInfoboxesRow = [[bigInfobox_name, bigInfobox_properties.shape[0], bigInfobox_properties.flatten()]]

    # saves bigger infoboxes
    biggerInfoboxes = pd.DataFrame(biggerInfoboxesRow, columns=biggerInfoboxesColumns, index=[categoryName])

    if (namesLength == 1):
        biggerInfoboxes.to_csv('results/csv/big-infoboxes.csv', mode='w', index=True, header=True, encoding='utf-8')
    else:
        with open('results/csv/big-infoboxes.csv', 'a') as f:
            biggerInfoboxes.to_csv(f, index=True, header=False, encoding='utf-8')


def saveStatisticsToFile(categoryName, categoriesResult, namesLength):
    print("saving statistics to file")

    categoriesResult = pd.DataFrame(categoriesResult, index=[categoryName], columns=columns)

    if (namesLength == 1):
        categoriesResult.to_csv('results/csv/general-statistics.csv', mode='w', index=True, header=True, encoding='utf-8')
    else:
        with open('results/csv/general-statistics.csv', 'a') as f:
            categoriesResult.to_csv(f, index=True, header=False, encoding='utf-8')


def saveInfoboxesSizeByCategoryToFile(categoryName, propertiesDistribution, namesLength):
    print("Saving infobox distribution to file")

    propertiesDistribution = [i for row in propertiesDistribution for i in row]

    infoboxDistribution = pd.DataFrame([propertiesDistribution], index=[categoryName])

    if (namesLength == 1):
        infoboxDistribution.to_csv('results/csv/temp-categories-infobox-distribution.csv', mode='w', index=True, header=False, encoding='utf-8')
    else:
        with open('results/csv/temp-categories-infobox-distribution.csv', 'a') as f:
            infoboxDistribution.to_csv(f, index=True, header=False, encoding='utf-8')


def plotInfoboxesSizeDist4SelectedCategories():
    infoboxesSizeByCategory = my_csv.readCSVFile('results/csv/temp-categories-infobox-distribution.csv')

    labels = []
    infoboxesDistribution = []

    for row in infoboxesSizeByCategory:
        label = row[0]
        distribution = row[1:]
        labels.append(label)
        infoboxesDistribution.append(map(int, distribution))

    # boxplot of infoboxes size by category
    v.plotInfoboxesSizeBoxplot(labels, infoboxesDistribution, "results/plots/distr/all-cat-infoboxes-size-dist.png")


def run():
    # Read datasets
    categoriesName = inp.readFiles(constants.infobox_datasets)

    names = []

    # Iterates over csv files and calculates infobox statistics
    for categoryName in categoriesName:

        category = my_csv.readCSVFile(constants.infobox_datasets+"/"+categoryName)
        categoryName = categoryName.replace(".csv","")
        names.append(categoryName)
        print("=================== %s ====================" % categoryName)

        # Big Infobox
        saveBigInfoboxesInfo(categoryName, category, len(names))

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
        props_missing_usage = np.mean(stat.getMissingUsage(propertiesProportion))

        # append to create csv file
        categoriesResult = [[articles_count, infoboxes_count, countArticlesWithGeoProps,
                             countArticlesWithDateTimeProps, common_props_count, average,
                             std, median, props_missing_usage]]

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

        # saves statistics into csv file
        saveStatisticsToFile(categoryName, categoriesResult, len(names))

        # Plot infoboxes size distribution per category
        propertiesDistribution = stat.getInfoboxesDistribution(category)

        saveInfoboxesSizeByCategoryToFile(categoryName, propertiesDistribution.values, len(names))

        v.plotInfoboxesDistribution(categoryName, propertiesDistribution, 'results/plots/distr')

        # get top 30 properties
        print("getting top 30 properties...")
        topProperties = stat.topPropertiesByProportion(category, 30, infoboxes_count)
        v.plotScatter(categoryName, topProperties, 'results/plots/scatter/', "Properties proportion: " + categoryName)


def runCompleteInfoboxSizeDistribution():
    print("plotting complete distribution of infoboxes size...")
    try:
        with open("results/csv/all_infoboxes_size.csv", 'r') as f:
            category = list(csv.reader(f, delimiter=","))
            infoboxesSize = pd.DataFrame(category).fillna(0).values.astype(np.int_)
            v.plotCompleteExtractionInfoboxesSizeBoxPlot(infoboxesSize, "results/plots/distr/infoboxes-size-complete.png")
    except IOError:
        print("results/csv/all_infoboxes_size.csv DO NOT EXISTS")

run()

runCompleteInfoboxSizeDistribution()

plotInfoboxesSizeDist4SelectedCategories();

print("FINISHED")
