import numpy as np
import pandas as pd

'''
	FOR GENERAL STATISTICS FROM PROPERTIES FROM INFOBOX EXTRACTIONS
'''

# counts articles, infoboxes and properties
def countElements(category):
	# subset matrix ignoring header and first column (article_name)
	articles = category[1:, 1:]
	countArticles, countProperties = articles.shape
	# count infoboxes (non-empty rows)
	infoboxes = articles[~np.all(articles==" ", axis=1)]
	countInfoboxes = infoboxes.shape[0]
	return countArticles, countInfoboxes, countProperties

# returns the average infobox properties for category
def averageInfoboxProperties(category):
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
	variance = np.around(np.var(countProperties), decimals=2)
	covariance = np.around(np.cov(countProperties), decimals=2)
	return average, std, median, variance, covariance

#returns a sorted dataframe of infobox properties
def sortedProperties(category):
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

#return a dataframe with the top N properties for category
def topProperties(category, topN):
	sort = sortedProperties(category)
	return sort.head(topN)

#return a dataframe with the proportion of top N properties for category
def topPropertiesByProportion(category, topN, infoboxCount):
	sort = sortedProperties(category)
	sort = sort / infoboxCount
	return sort.head(topN)

# returns article name and infobox properties from the biggest infobox in the categry
def getBiggerInfobox(category):
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

# returns a dattaframe with infobox distribution
def getInfoboxesDistribution(category):
	# subset matrix ignoring header and first column with articles name
	articles = category[1:, 1:]
	# subset just articles name
	articles_name = category[1:, 0]
	# count existing properties for each infobox
	countProperties = (articles!=' ').sum(axis=1)
	# distribution dataframe
	infoboxesDistribution = pd.DataFrame(countProperties, columns=['Count'], index=articles_name)
	infoboxesDistribution = infoboxesDistribution[infoboxesDistribution.Count!=0]
	#print(infoboxesDistribution)
	return infoboxesDistribution
