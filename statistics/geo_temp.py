import numpy as np
import pandas as pd
import util.properties_categories as props

'''
    FOR GEOGRAPHIC AND DATE/TIME STATISTICS FROM PROPERTIES FROM INFOBOX EXTRACTIONS
'''
def countDateTimeProps(category):
    header = category[0, 1:]
    infoboxes = category[1:, 1:]

    # removes all empty rows (articles without infobox)
    infoboxes = infoboxes[~np.all(infoboxes==' ', axis=1)]

    # switch values in rows by its respective column name
    infoboxes = [ header[np.where(infoboxes[ row, : ]!=' ' )] for row in range(0, infoboxes.shape[0]) ]
    infoboxes = [ item.tolist() for item in infoboxes]

    countYear = 0
    countDate = 0
    countPeriod = 0
    countTime = 0
    countMonth = 0

    for infobox in infoboxes:
        countYear = countYear + np.isin(infobox, props.year).sum(axis=0)
        countDate = countDate + np.isin(infobox, props.date).sum(axis=0)
        countPeriod = countPeriod + np.isin(infobox, props.period).sum(axis=0)
        countTime = countTime + np.isin(infobox, props.time).sum(axis=0)
        countMonth = countMonth + np.isin(infobox, props.month).sum(axis=0)

    datetimeTotal = countYear + countDate + countPeriod + countTime + countMonth

    countProperties = [countYear, countDate, countPeriod, countTime, countMonth]

    properties_name = np.array(["Year", "Date", "Period", "Time", "Month"])

    count_props = (pd.DataFrame(countProperties, columns=['Count'], index=properties_name) / datetimeTotal).fillna(0)

    return count_props[count_props.Count != 0]

def countGeographicProps(category):

    header = category[0, 1:]
    infoboxes = category[1:, 1:]

    # removes all empty rows (articles without infobox)
    infoboxes = infoboxes[~np.all(infoboxes==' ', axis=1)]

    # switch values in rows by its respective column name
    infoboxes = [ header[np.where(infoboxes[ row, : ]!=' ' )] for row in range(0, infoboxes.shape[0]) ]
    infoboxes = [ item.tolist() for item in infoboxes]

    countLatitude = 0
    countLongitude = 0
    countLocation = 0
    countArea = 0
    countCoord = 0
    countAltitude = 0
    countOther = 0
    for infobox in infoboxes:
        countLatitude = countLatitude + np.isin(infobox, props.latitudeProps).sum(axis=0)
        countLongitude = countLongitude + np.isin(infobox, props.longitudeProps).sum(axis=0)
        countLocation = countLocation + np.isin(infobox, props.locationProps).sum(axis=0)
        countArea = countArea + np.isin(infobox, props.areaProps).sum(axis=0)
        countCoord = countCoord + np.isin(infobox, props.coordinatesProps).sum(axis=0)
        countAltitude = countAltitude + np.isin(infobox, props.altitudeProps).sum(axis=0)
        countOther = countOther + np.isin(infobox, props.otherProps).sum(axis=0)

    geopropertiesTotal = countLatitude + countLongitude + countLocation + countArea + countCoord + countAltitude + countOther

    countProperties = [countLatitude, countLongitude, countLocation, countArea, countCoord, countAltitude, countOther]

    properties_name = np.array(["Latitude", "Longitude", "Location", "Area", "Coordinates", "Altitude", "Specific"])

    count_props = (pd.DataFrame(countProperties, columns=['Count'], index=properties_name) / geopropertiesTotal).fillna(0)

    return count_props[count_props.Count != 0]

# get geo properties from category header
def getHeaderGeoProps(category):	
    header = category[0, 1:]
    geographicProps = np.in1d(header, props.geoPropertiesNames, assume_unique=True)
    return geographicProps

# get articles with geographic information related
def getGeoProps(category):

    # get geographic props index
    geographicProps = getHeaderGeoProps(category)

    # ignores first column (articles name) and first row (header)
    articles = category[1:,1:]

    # remove lines were all columns for properties are empty
    has_values = articles[~np.all(articles==" ", axis=1)]

    # subset rows from category with a geographic value associated
    articlesWithGeographicProps = has_values[:, geographicProps]

    # remove articles with no geographic information related
    articlesWithGeoProps = articlesWithGeographicProps[~np.all(articlesWithGeographicProps==" ", axis=1)]

    return articlesWithGeoProps

# get temporal properties from category header
def getHeaderDateTimeProps(category):	
    header = category[0,1:]
    geographicProps = np.in1d(header, props.dateTimePropertiesNames, assume_unique=True)
    return geographicProps

# get articles with temporal information related
def getDateTimeProps(category):
    # get temporal props index
    dateTimeProps = getHeaderDateTimeProps(category)

    # ignores first column (articles name) and first row (header)
    articles = category[1:,1:]

    # remove lines were all columns for properties are empty
    has_values = articles[~np.all(articles==" ", axis=1)]

    # subset rows from category with temporal value associated
    articlesWithDateTimeProps = has_values[:, dateTimeProps]

    # remove articles with no temporal information related
    articlesWithDateTimeProps = articlesWithDateTimeProps[~np.all(articlesWithDateTimeProps==" ", axis=1)]

    return articlesWithDateTimeProps

# count articles with properties and total of props in category
def count(articlesWithProps, countArticles, countInfoboxes, countProperties):
    countArticlesWithProps, countProps = articlesWithProps.shape
    return countArticlesWithProps, countProps

# top properties
def getSort(articlesWithProps):
    properties_name = articlesWithProps[0,:]
    countProperties = (articlesWithProps!=" ").sum(axis=0)
    countProperties = pd.DataFrame(countProperties, columns=['Count'], index=properties_name)
    sortedProperties = countProperties.sort_values(by="Count", axis=0, ascending=False)
    return sortedProperties

# returns a dataframe with the proportion of top N properties for category
def topPropertiesByProportion(articlesWithProps, topN, infoboxCount):
    sorting = getSort(articlesWithProps)
    sort = sorting / infoboxCount
    return sort.head(topN)

# returns a dataframe with the proportion of top N properties for category
def getSortedProperties(articlesWithProps, infoboxCount):
    sorting = getSort(articlesWithProps)
    sort = sorting / infoboxCount
    return sort
