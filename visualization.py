import numpy as np
import matplotlib.pyplot as plt

def plotScatter(categoryName, topProps, path):
	x_ticks = np.arange(1, topProps.shape[0] + 1, 1);
	y = topProps['Count']
	plt.xticks(x_ticks, topProps.index.values, rotation='vertical')
	plt.grid(linestyle='dotted', alpha=0.5)
	colors = y
	area = 150 * y*3
	plt.scatter( x_ticks, y, c=colors, s=area, alpha=0.9, cmap=plt.cm.cool)
	plt.title("Infobox properties frequency for %s" % categoryName)
	plt.ylabel("Frequency")
	plt.xlabel("Properties")
	plt.savefig(path+categoryName+'.png', bbox_inches='tight')
	plt.gcf().clear()
	plt.cla()
	plt.clf()
	plt.close()
