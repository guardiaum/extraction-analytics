import util.my_csv as csv
import plotting.visualization as v
import util.constants as constants
import statistics.common as stat
import util.input as inp
import clustering.hac_complete_linkagematrix as complete
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist

'''
    CLUSTERING EXECUTION
    FOR GROUP OF CATEGORIES 
    It is required to inform categoriesName, output file name, title for plot and subtitle if needed
'''

categoriesLinkage = [] # Linkage vector for plot a group

# Read datasets name
categoriesName, outputFileName, title, subtitle = inp.readGroupOfFiles(constants.infobox_datasets)

for categoryName in categoriesName:
    category = csv.readCSVFile(constants.infobox_datasets+"/"+categoryName)

    print("Start clustering: %s ====================" % categoryName)

    category = complete.preprocessDataset(category) # Preprocess datasets for plotting
    distanceMatrix = pdist(category, 'jaccard')
    #print(distanceMatrix)
    categoriesLinkage.append([categoryName, distanceMatrix])

print("Plotting...")

# plot boxplot similarities
v.plotBoxplot(categoriesLinkage, 'results/plots/boxplots/'+outputFileName+'.png', title, subtitle);

print("FINISHED")
