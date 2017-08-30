from clustering.cluster import Cluster
from sklearn import metrics
from datetime import datetime
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
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
				
	aux = articles.tolist()
	clusters = []
	for c in aux:
		cluster = Cluster(c, active=True)
		clusters.append(cluster)
		
	#for c in clusters:
	#	print(c.active)
	return clusters
	
# filter dataset by top properties
# replace property values by equivalent property name on each row
# removes empty rows (articles without infobox instance)
# converts numpy array to list
def preprocessDatasetTopProps(category, topProperties):
	properties = topProperties.index.values # get top property names
	header = category[0, 0:] # separates property names
	properties = np.in1d(header, properties, invert=True) # verifies which header properties are not top properties
	indexes = np.where(properties) # get indexes of header properties that are not top properties
	category = np.delete(category, indexes, 1) # removes columns from not top properties
	newHeader = category[0, 0:]
	articles = category[1:, 0:] # removes the header
	articles = articles[~np.all(articles==" ", axis=1)] # removes empty rows (articles without infobox)
	rows, cols = articles.shape 
	# replace property value by its respective property name
	for x in range(0, rows):
		for y in range(0, cols):
			if(articles[x, y]!=" "):
				articles[x, y] = newHeader[y]
	
	aux = articles.tolist()
	clusters = []
	for c in aux:
		cluster = Cluster(c, active=True)
		clusters.append(cluster)
		
	#for c in clusters:
	#	print(c.active)
	return clusters

# calculates jaccard similarity btw two clusters
def jaccardSimilarity(art1, art2):
	similarity = 0.00
	count = 2
	# both arguments are single clusters
	if(type(art1[0]) is str and type(art2[0]) is str):
		similarity = metrics.jaccard_similarity_score(art1, art2)
		count = 2
	# first argument is a collection of clusters
	# recursively calculates similarity for each cluster from collection
	# and the second argument. Returns major similarity
	elif(type(art1[0]) is not str and type(art2[0]) is str):
		for i in range(0, len(art1)):
			clusterSimilarity, countAux = jaccardSimilarity(art1[i], art2)
			if(similarity < clusterSimilarity):
				similarity = clusterSimilarity
				count = countAux + 1
	# does the same for second argument beein a collection of clusters
	elif(type(art2[0]) is not str and type(art1[0]) is str):
		for i in range(0, len(art2)):
			clusterSimilarity, countAux = jaccardSimilarity(art1, art2[i])
			if(similarity < clusterSimilarity):
				similarity = clusterSimilarity
				count = countAux + 1
	# both arguments are a cluster collection
	elif(type(art1[0]) is not str and type(art1[0]) is not str):
		for i in range(0, len(art1)):
			for j in range(0, len(art2)):
				clusterSimilarity, countAux = jaccardSimilarity(art1[i], art2[j])
				if(similarity < clusterSimilarity):
					similarity = clusterSimilarity
					count = countAux
	return similarity, count

# finds the maximum similarities btw clusters on 
# dataset and merges into one single cluster
def mergeMatrix(clusters, matrix):
	maxSimilarity = 0.00
	cluster1Index = -1
	cluster2Index = -1
	count = 0
	
	#calculates similarity matrix
	for i in range(0, len(clusters)):
		for j in range( i + 1, len(clusters)):
			if((clusters[ i ].active==True) and (clusters[ j ].active == True)):
				similarity, countAux = jaccardSimilarity( clusters[ i ], clusters[ j ] )
				if(maxSimilarity < similarity ):
					maxSimilarity = similarity
					cluster1Index = i
					cluster2Index = j
					count = countAux
	
	#updates clusters and updates linkage matrix
	if(cluster1Index!=-1 and cluster2Index!=-1 and maxSimilarity!=0.00):
		i = 0 
		while(i<len(matrix)):
			if(matrix[i]!=None):
				i = i + 1
			else:
				matrix[i] = [cluster1Index, cluster2Index, maxSimilarity, count]
				break;
		
		c = [clusters[cluster1Index], clusters[cluster2Index]]
		new = Cluster(c, active=True)
		clusters.append(new)
		clusters[cluster1Index].active = False
		clusters[cluster2Index].active = False
		#print("Clusters collection: %s" % len(clusters))
		if(clusters[len(clusters)-1].active==True):
			clusters, matrix = mergeMatrix(clusters, matrix)
			
	return clusters, matrix

def agglomerateAllProperties(category):
	trun = datetime.now()
	print("Start clustering %s" %  trun)
	clusters = preprocessDataset(category)
	matrixsize = len(clusters) - 1
	matrix = [ None for y in range( matrixsize ) ]
	clusters, matrix = mergeMatrix( clusters, matrix )
	tend = datetime.now()
	processtime = tend - trun
	
	#print( "Cluster >>> %s" % clusters ) 
	print( "Matrix >>> %s" % matrix )
	#print( "Size Matrix >>> %s" % len(matrix) )
	
	print("Finished clustering > Time spent: %s" % processtime)
	return clusters, matrix
	
def agglomerateTopProperties(category, topProperties):
	trun = datetime.now()
	print("Start clustering %s" %  trun)
	clusters = preprocessDatasetTopProps(category, topProperties)
	matrixsize = len(clusters) - 1
	matrix = [ None for y in range( matrixsize ) ]
	clusters, matrix = mergeMatrix( clusters, matrix )
	tend = datetime.now()
	processtime = tend - trun
	'''
	print( "Matrix >>> %s" % matrix )
	print( "Size Matrix >>> %s" % len(matrix) )
	plt.figure()
	dn = hierarchy.dendrogram(matrix, distance_sort='descending')
	plt.savefig('dendogram.png', bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()
	'''	
	print("Finished clustering > Time spent: %s" % processtime)
	return clusters, matrix
	
