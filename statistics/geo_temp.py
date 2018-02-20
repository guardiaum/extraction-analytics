import numpy as np
import pandas as pd
import util.constants as constants
import re

'''
    FOR GEOGRAPHIC AND DATE/TIME STATISTICS FROM PROPERTIES FROM INFOBOX EXTRACTIONS
'''
def countDateTimeProps(category):
    header = category[0, 1:]
    infoboxes = category[1:, 1:]

    # removes all empty rows (articles without infobox)
    infoboxes = infoboxes[~np.all(infoboxes==' ', axis=1)]

    # switch values in rows by its respective column name
    infoboxes = [header[np.where(infoboxes[ row, : ]!=' ' )] for row in range(0, infoboxes.shape[0])]
    infoboxes = [item.tolist() for item in infoboxes]

    countDate = 0
    countPeriod = 0
    countTime = 0

    for infobox in infoboxes:
        countDate = countDate + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.datetime_props_dict['date'])]).shape[0]
        countPeriod = countPeriod + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.datetime_props_dict['period'])]).shape[0]
        countTime = countTime + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.datetime_props_dict['time'])]).shape[0]

    datetimeTotal = countDate + countPeriod + countTime

    countProperties = [countDate, countPeriod, countTime]

    properties_name = np.array(["Date", "Period", "Time"])

    count_props = (pd.DataFrame(countProperties, columns=['Count'], index=properties_name) / datetimeTotal).fillna(0)
    print count_props

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
    countCoord = 0
    countMap = 0
    countOther = 0
    for infobox in infoboxes:
        countLatitude = countLatitude + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.geo_props_dict['latitude'])]).shape[0]
        countLongitude = countLongitude + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.geo_props_dict['longitude'])]).shape[0]
        countCoord = countCoord + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.geo_props_dict['coordinates'])]).shape[0]
        countLocation = countLocation + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.geo_props_dict['location'])]).shape[0]
        countMap = countMap + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.geo_props_dict['map'])]).shape[0]
        countOther = countOther + np.array([prop for prop in infobox
                                         if any(re.compile(propName).match(prop)
                                                for propName in constants.geo_props_dict['other'])]).shape[0]

    geopropertiesTotal = countLatitude + countLongitude + countLocation + countCoord + countMap + countOther

    countProperties = [countLatitude, countLongitude, countCoord, countLocation, countMap, countOther]

    properties_name = ['latitude', 'longitude', 'coordinates', 'location', 'map', 'other']

    count_props = (pd.DataFrame(countProperties, columns=['Count'], index=properties_name) / geopropertiesTotal).fillna(0)
    print count_props

    return count_props[count_props.Count != 0]


# get temporal properties from category header
def getHeaderDateTimeProps(category):
    header = category[0,1:]

    dateTimeProps = [prop for prop in header
                       if any(re.compile(propName).match(prop) for propName in constants.datetime_props_dict_all)]

    return np.isin(header, dateTimeProps)


# get geo properties from category header
def getHeaderGeoProps(category):
    header = category[0, 1:]

    geographicProps = [prop for prop in header
                       if any(re.compile(propName).match(prop) for propName in constants.geo_props_dict_all)]

    return np.isin(header, geographicProps)


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
