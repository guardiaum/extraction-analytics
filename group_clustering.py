import util.my_csv as csv
import plotting.visualization as v
import util.input as inp
import clustering.hac_complete_linkagematrix as complete
from scipy.cluster.hierarchy import linkage

'''
	CLUSTERING EXECUTION
	FOR GROUP OF CATEGORIES 
	It is required to inform categoriesName, output file name, title for plot and subtitle if needed
'''

categoriesLinkage = [] # Linkage vector for plot a group

categoriesName, outputFileName, title, subtitle = inp.readGroupOfFiles() # Read datasets name

for categoryName in categoriesName:
	category = csv.readCSVFile("datasets/"+categoryName)
	
	print("Start clustering: %s ====================" % categoryName)
	
	category = complete.preprocessDataset(category) # Preprocess datasets for plotting
	linkagematrix = linkage(category, method='complete', metric='jaccard') # calculates linkage matrix
	v.plotDendrogram('results/plots/cluster/', linkagematrix, categoryName) # plot dendrogram for single category
	categoriesLinkage.append([categoryName, linkagematrix[:, 2]])

print("Plotting...")

# plot boxplot similarities
v.plotBoxplot(categoriesLinkage, 'results/plots/boxplots/'+outputFileName+'.png', title, subtitle);

print("FINISHED")
