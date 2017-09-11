import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, fcluster, to_tree

def plotScatter(categoryName, topProps, path, title):
	x_ticks = np.arange(1, topProps.shape[0] + 1, 1)
	y = topProps['Count']
	plt.xticks(x_ticks, topProps.index.values, rotation='vertical')
	plt.grid(linestyle='dotted', alpha=0.5)
	colors = y
	plt.scatter( x_ticks, y, c=colors, s=30, alpha=0.9, cmap=plt.cm.cool)
	plt.title(title)
	plt.ylabel("Proportion")
	plt.xlabel("Properties")
	plt.savefig(path+categoryName+'.png', bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()

def plotBar(categoryName, props, path, title):
	y = range(len(props))
	labels = props.index.values
	fig, ax = plt.subplots()
	plt.barh(y, props['Count'], 0.5, color="gray", align='center', edgecolor="black", alpha=0.6)
	plt.yticks(y, labels)
	plt.tick_params(axis='both', which='major', labelsize=8)
	plt.tick_params(axis='both', which='minor', labelsize=6)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['left'].set_visible(False)
	plt.title(title)
	plt.xlabel("Proportion")
	plt.ylabel("Properties")
	plt.savefig(path+categoryName+'.png', bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()

def plotDendrogram(filepath, linkagematrix, categoryname):
	plt.figure(figsize=(25, 10))
	plt.title('Hierarchical Clustering Dendrogram')
	plt.xlabel('sample index')
	plt.ylabel('distance')
	dendrogram(
	    linkagematrix,
	    leaf_rotation=90.,  # rotates the x axis labels
	    leaf_font_size=8.,  # font size for the x axis labels
	)
	filename = filepath + 'DENDROGRAM-' + categoryname + '.png'
	plt.savefig(filename, bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()

def plotTree(linkagematrix, categoryname):
	rootnode, nodelist = to_tree(linkagematrix, rd=True)
	print("NodeList: %s" % len(nodelist))
	return rootnode, nodelist
	
def plotInfoboxesDistribution(categoryName, infoboxesDist, filepath, title):
	fig, ax = plt.subplots()
	
	filename = filepath + '/infobox-distribution-' + categoryName + '.png'
	#num_bins = (infoboxesDist.shape[0])
	properties_count = infoboxesDist.Count
	
	#calculates mean and standard deviation of distribution
	mu = np.around(np.mean(properties_count), decimals=2)
	sigma = np.around(np.std(properties_count), decimals=2)
	
	# the histogram of the data
	n, bins, patches = ax.hist(properties_count, normed=1, alpha=0.7)
	
	# add a 'best fit' line
	y = mlab.normpdf(bins, mu, sigma)
	ax.plot(bins, y, '--')
	
	# set axes and title
	ax.set_xlabel("Properties")
	ax.set_ylabel("Infobox density")
	
	plt.suptitle(title, fontsize=12)
	subtitle = r'Histogram of {0}: $\mu={1}$, $\sigma={2}$'.format(categoryName, mu,  sigma)
	plt.title(subtitle, fontsize=9)
	
	# save plot
	plt.savefig(filename, bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()
	
def plotBoxplot(categoriesSimilarities, filepath, title, subtitle):
	categoriesName = []
	data_to_plot = []
	for index, category in enumerate(categoriesSimilarities):
		x = index + 1
		data_to_plot.append(category[1])
		categoriesName.append(category[0])	
	
	fig = plt.figure(1, figsize=(9, 6))
	# Create an axes instance
	ax = fig.add_subplot(111)
	# Create the boxplot
	bp = ax.boxplot(data_to_plot)
	
	ax.set_xticklabels(categoriesName)
	
	plt.suptitle(title, fontsize=12)
	plt.title(subtitle, fontsize=10)
	
	# save plot
	plt.savefig(filepath, bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()
