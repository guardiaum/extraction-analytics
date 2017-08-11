import numpy as np
import pandas as pd

geoPropertiesNames = np.array(['locationMap', 'locationMapSize', 'latD', 'latM', 'latS', 'latNs', 'longD', 'longM', 'longS', 'longEw','coordinatesType', 'coordinatesDisplay', 'coordinatesFormat', 'coordinatesRegion', 'country', 'city', 'area', 'coordinatesRef', 'latitude', 'longitude', 'latDeg', 'latMin', 'latMax', 'lonDeg', 'latSec', 'latDir', 'lonMin', 'lonSec','lonDir', 'latd', 'latm', 'lats', 'latns', 'longd', 'longm', 'longs', 'longew', 'location', 'region', 'lat', 'long', 'latDegrees', 'latMinutes', 'latSeconds', 'latDirection', 'longDegrees', 'longMinutes', 'longSeconds', 'longDirection', 'coordDisplay', 'coordParameters', 'birthPlace'])

dateTimePropertiesNames = np.array(['years', 'year', 'date', 'birthDate', 'electionDate', 'timestamp', 'time', 'duration' ])

# get geo properties from category header
def getHeaderGeoProps(category):	
	header = category[0,1:]
	geographicProps = np.in1d(header, geoPropertiesNames, assume_unique=True)
	return geographicProps

# get articles with geographic information related
def getGeoProps(category):
	articles = category[0:,1:]
	# remove lines were all columns for properties are empty
	has_values = articles[~np.all(articles==" ", axis=1)]
	# get geographic props index
	geographicProps = getHeaderGeoProps(category)
	#subset rows from category with a geographic value associated
	articlesWithGeographicProps = has_values[:, geographicProps]
	#remove articles with no geographic information related
	articlesWithGeoProps = articlesWithGeographicProps[~np.all(articlesWithGeographicProps==" ", axis=1)]
	return articlesWithGeoProps

# get temporal properties from category header
def getHeaderDateTimeProps(category):	
	header = category[0,1:]
	geographicProps = np.in1d(header, dateTimePropertiesNames, assume_unique=True)
	return geographicProps

# get articles with temporal information related
def getDateTimeProps(category):
	articles = category[0:,1:]
	# remove lines were all columns for properties are empty
	has_values = articles[~np.all(articles==" ", axis=1)]
	# get temporal props index
	dateTimeProps = getHeaderDateTimeProps(category)
	#subset rows from category with temporal value associated
	articlesWithDateTimeProps = has_values[:, dateTimeProps]
	#remove articles with no temporal information related
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
