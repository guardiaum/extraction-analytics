import util.my_csv as csv
import statistics.common as stat
import statistics.geo_temp as prop
import plotting.visualization as v
import pandas as pd
import clustering.hac_single_linkagematrix as single
import clustering.hac_complete_linkagematrix as complete
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial import distance
import numpy as np

'''
	FOR GROUP OF CATEGORIES CLUSTERING EXECUTION
	It is required to inform categoriesName and filename
'''

categories = []
categoriesLinkage = []
columns = ["Count Articles", "Count Infoboxes", "Count Infob. w/ Geoinfo", "Count infob. w/ Datetime","Count Total Properties", "Count Geo Props.", "Count datetime props", "Avg. Properties", "std props", "median props", "var props", "cov props"]

# iterates over csv files, clustering the categories and plotting the result
categoriesName = ["Geothermal_power_stations", "Natural_gas_fields", "Protein_domains"]
filename = 'AVERAGE-geo-gas-protein_clustering_plot'

for categoryName in categoriesName:
	category = csv.readCSVFile("datasets/"+categoryName+".csv")
	print("Start clustering: %s ====================" % categoryName)
	category = complete.preprocessDataset(category)
	linkagematrix = linkage(category, method='average', metric='jaccard')
	categoriesLinkage.append([categoryName, linkagematrix])
	v.plotSimilarity(linkagematrix, categoryName)
print("Plotting...")

v.plotThree(categoriesLinkage, filename);

print("FINISHED")
