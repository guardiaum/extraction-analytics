import numpy as np
import random
import matplotlib.pyplot as plt

def plotScatter(categoryName, topProps, path, title):
	x_ticks = np.arange(1, topProps.shape[0] + 1, 1);
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
	x = range(len(props))
	labels = props.index.values
	width = 1/1.8
	plt.bar(x, props['Count'], width, color="gray")
	plt.xticks(x, labels, rotation='vertical')
	plt.title(title)
	plt.ylabel("Proportion")
	plt.xlabel("Properties")
	plt.savefig(path+categoryName+'.png', bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()
	
def plotThree(similarities, filename):
	# Create traces
	data = []
	fig, ax = plt.subplots()
	markers = ['-o', '--v', '-.^', ':s', '->', ':d', '-.h']
	for similarity in similarities:
		similarity_vector = np.array(similarity[1])
		onlySimilarities = similarity_vector[:,2]
		similarityRegulated, count = np.unique(onlySimilarities, return_counts=True)
		soma = (np.sum(count, axis=0))
		y_axis = np.array(count) / float(soma)
		markerIndex = random.randint(0, len(markers)-1)
		plt.plot(similarityRegulated, y_axis, markers[markerIndex], label=similarity[0])
	ax.legend()
	plt.title("Infoboxes schema diversity for categories")
	plt.ylabel("Clusters Proportion")
	plt.xlabel("Clusters Similarities")
	filename = 'logs/%s.png' % filename
	plt.savefig(filename, bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()
