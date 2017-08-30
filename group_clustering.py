import util.my_csv as csv
import statistics.common as stat
import statistics.geo_temp as prop
import plotting.visualization as v
import pandas as pd
import clustering.hac_single_linkagematrix as single
import clustering.hac_complete_linkagematrix as complete

'''
	FOR GROUP OF CATEGORIES CLUSTERING EXECUTION
	It is required to inform categoriesName and filename
'''

categories = []
linkagematrixes = []
columns = ["Count Articles", "Count Infoboxes", "Count Infob. w/ Geoinfo", "Count infob. w/ Datetime","Count Total Properties", "Count Geo Props.", "Count datetime props", "Avg. Properties", "std props", "median props", "var props", "cov props"]

# iterates over csv files, clustering the categories and plotting the result
categoriesName = ["Geothermal_power_stations", "Natural_gas_fields", "Protein_domains"]
filename = 'geo-gas-protein_clustering_plot'

for categoryName in categoriesName:
	category = csv.readCSVFile("datasets/"+categoryName+".csv")
	
	print("Start clustering: %s ====================" % categoryName)
	clusters, linkagematrix = single.agglomerateAllProperties( category )
	linkage = [categoryName, linkagematrix]
	linkagematrixes.append(linkage)
	print("linkage matrix >> %s" %linkagematrix)

print("Plotting...")
categoriesLinkage = []
for info in linkagematrixes:
	categoryName = info[0]
	linkageMatrix = np.array(info[1])
	similarities = linkageMatrix[:,2]
	categoriesLinkage.append([categoryName, similarities])

v.plotThree(categoriesLinkage, filename);

print("FINISHED")
