import util.my_csv as csv
import plotting.visualization as v
import util.constants as constants
import util.input as inp
import clustering.hac_complete_linkagematrix as complete
from scipy.spatial.distance import pdist
import sys

'''
    INFOBOX HOMOGENEITY IN CATEGORY
    FOR GROUP OF CATEGORIES 
    Measures how similar are the infoboxes in a given category
    It is required to inform categoriesName, output file name, title for plot and subtitle if needed
'''

categoriesLinkage = [] # Linkage vector for plot a group

# Read datasets name
categoriesName = inp.readFiles(constants.infobox_datasets)

if len(sys.argv) == 3:
    numberOfChunks = int(sys.argv[1])
    chunk2select = int(sys.argv[2]) - 1

    chunks = inp.chunkIt(categoriesName, numberOfChunks)

    categoriesName = chunks[chunk2select]

    print(chunks)
    print(categoriesName)

for categoryName in categoriesName:

    category = csv.readCSVFile(constants.infobox_datasets+"/"+categoryName)

    categoryName = categoryName.replace(".csv", "")
    print("Start clustering: %s ====================" % categoryName)

    category = complete.preprocessDataset(category) # Preprocess datasets for plotting
    distanceMatrix = pdist(category, 'jaccard')
    categoriesLinkage.append([categoryName, distanceMatrix])

print("Plotting...")

# plot boxplot similarities
v.plotBoxplot(categoriesLinkage, 'results/plots/quality/infoboxes-homogeneity-all.png');

print("FINISHED")
