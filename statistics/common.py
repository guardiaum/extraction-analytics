import numpy as np
import pandas as pd


'''
    FOR GENERAL STATISTICS FROM PROPERTIES FROM INFOBOX EXTRACTIONS
'''


def getArticlesWithInfoboxScheme(category):
    header = category[0, :]
    articles = category[1:, 1:]
    category = category[1:, :]

    # subset by infoboxes (non-empty rows)
    # remove lines were all columns for properties are empty
    infoboxesWithoutArticleName = ~np.all(articles==" ", axis=1)

    infoboxes = category[np.where(infoboxesWithoutArticleName)]

    rows, cols = infoboxes.shape
    # replace property value by its respective property name
    for x in range(0, rows):
        for y in range(1, cols): #ignores first column containing article name
            if(infoboxes[x, y]!=" "):
                infoboxes[x, y] = header[y]
    return infoboxes


def countElements(category):  # counts articles, infoboxes and properties
    # subset matrix ignoring header and first column (article_name)
    articles = category[1:, 1:]
    countArticles, countProperties = articles.shape
    # count infoboxes (non-empty rows)
    infoboxes = articles[~np.all(articles==" ", axis=1)]
    countInfoboxes = infoboxes.shape[0]
    return countArticles, countInfoboxes, countProperties


def averageInfoboxProperties(category):  # returns the average infobox properties for category
    # subset matrix ignoring header and first column (article_name)
    articles = category[1:, 1:]
    # subset by infoboxes (non-empty rows)
    # remove lines were all columns for properties are empty
    has_infobox = articles[~np.all(articles==" ", axis=1)]
    # count existing properties for each infobox
    countProperties = (has_infobox!=" ").sum(axis=1)
    average = np.around(np.mean(countProperties), decimals=2)
    std = np.around(np.std(countProperties), decimals=2)
    median = np.around(np.median(countProperties), decimals=2)
    #variance = np.around(np.var(countProperties), decimals=2)
    #covariance = np.around(np.cov(countProperties), decimals=2)
    return average, std, median #, variance, covariance


def sortedProperties(category):  #returns a sorted dataframe of infobox properties
    # subsets articles without articles name column
    articles = category[:, 1:]
    # gets properties name from header
    properties_name = articles[0, :]
    # count property across each row (infobox)
    countProperties = (articles!=" ").sum(axis = 0) - 1
    # creates dataframe with properties distribution
    countProperties = pd.DataFrame(countProperties, columns=['Count'], index=properties_name)
    sortedProperties = countProperties.sort_values(by="Count", axis=0, ascending=False)
    return sortedProperties


def topProperties(category, topN):  #return a dataframe with the top N properties for category
    sort = sortedProperties(category)
    return sort.head(topN)


def topPropertiesByProportion(category, topN, infoboxCount):  #return a dataframe with the proportion of top N properties for category
    sort = sortedProperties(category)
    sort = sort / infoboxCount
    return sort.head(topN)


def propertiesProportion(category, infoboxCount):  #return a dataframe with properties proportion for category
    sort = sortedProperties(category)
    sort = sort / infoboxCount
    return sort


def getBiggerInfobox(category):  # returns article name and infobox properties from the biggest infobox in the category
    # header without article_name
    header = category[0, 1:]
    # subset matrix ignoring header
    articles = category[1:, :]
    # count existing properties for each infobox
    countProperties = (articles!=' ').sum(axis=1)
    biggerInfoboxIndex = np.argmax(countProperties)
    # subset matrix ignoring only the header
    biggerInfobox = articles[biggerInfoboxIndex, :]
    article_name = biggerInfobox[0]
    infobox_properties = header[np.where(biggerInfobox[1:])]
    #print(article_name)
    #print(infobox_properties)
    return article_name, infobox_properties

# Counts the amount of properties exist in each infobox
# returns a dataframe with infoboxes size
def getInfoboxesDistribution(category):
    # gets articles and articles name
    articles = category[1:, 0:]

    # subset just articles name
    articles_name = articles[1:, 0]

    # subset articles recovering only properties
    articles_props = articles[1:, 1:]

    # count properties appearences in all articles
    countProperties = (articles_props != ' ').sum(axis=1)

    # distribution dataframe
    infoboxesDistribution = pd.DataFrame(countProperties, columns=['Count'], index=articles_name)

    return infoboxesDistribution[infoboxesDistribution.Count!=0]


def getMissingUsage(propertiesProportion):
    missUsage = 1.0 - propertiesProportion['Count']
    return np.around(missUsage, decimals=2)


def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation 
    """
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))
