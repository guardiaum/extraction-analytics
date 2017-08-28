from sklearn import metrics
from datetime import datetime
import numpy as np

# replace property values by equivalent property name on each row
# removes empty rows (articles without infobox instance)
# converts numpy array to list
def preprocessDataset(category):
	header = category[0, 1:] # separates property names
	articles = category[1:, 1:] # remove header and article names
	articles = articles[~np.all(articles==" ", axis=1)] # removes empty rows (articles without infobox)
	rows, cols = articles.shape 
	# replace property value by its respective property name
	for x in range(0, rows):
		for y in range(0, cols):
			if(articles[x, y]!=" "):
				articles[x, y] = header[y]
	return articles.tolist()

# calculates jaccard similarity btw two clusters
def jaccardSimilarity(art1, art2):
	similarity = 0.00
	# both arguments are single clusters
	if(type(art1[0]) is str and type(art2[0]) is str):
		similarity = metrics.jaccard_similarity_score(art1, art2)
	# first argument is a collection of clusters
	# recursively calculates similarity for each cluster from collection
	# and the second argument. Returns major similarity
	elif(type(art1[0]) is not str and type(art2[0]) is str):
		for i in range(0, len(art1)):
			clusterSimilarity = jaccardSimilarity(art1[i], art2)
			if(similarity < clusterSimilarity):
				similarity = clusterSimilarity
	# does the same for second argument beein a collection of clusters
	elif(type(art2[0]) is not str and type(art1[0]) is str):
		for i in range(0, len(art2)):
			clusterSimilarity = jaccardSimilarity(art1, art2[i])
			if(similarity < clusterSimilarity):
				similarity = clusterSimilarity
	# both arguments are a cluster collection
	elif(type(art1[0]) is not str and type(art1[0]) is not str):
		for i in range(0, len(art1)):
			for j in range(0, len(art2)):
				clusterSimilarity = jaccardSimilarity(art1[i], art2[j])
				if(similarity < clusterSimilarity):
					similarity = clusterSimilarity
	return similarity

# finds the maximum similarities btw clusters on 
# dataset and merges into one single cluster
def findMaxSimilarity(clusters):
	maxSimilarity = 0.00
	cluster1Index = -1
	cluster2Index = -1
	
	for i in range(0, len(clusters)):
		for j in range( i + 1, len(clusters)):
			similarity = jaccardSimilarity( clusters[ i ], clusters[ j ] )
			if(similarity > maxSimilarity):
				maxSimilarity = similarity
				cluster1Index = i
				cluster2Index = j
	
	if(cluster1Index!=-1 and cluster2Index!=-1):
		clusters[cluster1Index] =  [clusters[cluster1Index], clusters[cluster2Index]]
		del clusters[cluster2Index]
		print("Clusters collection: %s" % len(clusters))
		if(len(clusters) > 1):
			clusters = findMaxSimilarity(clusters)
		
	return clusters

def agglomerateAllProperties(category):
	trun = datetime.now()
	print("Start clustering %s" %  trun)
	clusters = preprocessDataset(category)
	mergeMatrix = findMaxSimilarity( clusters )
	tend = datetime.now()
	processtime = tend - trun
	print( "Cluster >>> %s" % mergeMatrix )
	print("Time spent: %s" % processtime)
	return mergeMatrix
