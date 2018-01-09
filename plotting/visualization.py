import numpy as np
import pandas as pd
from itertools import compress
from pylab import *
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


def plotInfoboxesDistribution(categoryName, infoboxesDist, filepath):
    fig, ax = plt.subplots()
    filename = filepath + '/infobox-distribution-' + categoryName + '.png'
    properties_count = infoboxesDist.Count

    #calculates mean and standard deviation of distribution
    mu = np.around(np.mean(properties_count), decimals=2)
    sigma = np.around(np.std(properties_count), decimals=2)

    # the histogram of the data
    n, bins, patches = ax.hist(properties_count, normed=1, facecolor="#d7c400", alpha=0.9)

    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    ax.plot(bins, y, '--')

    # set axes and title
    ax.set_xlabel("Count properties")
    ax.set_ylabel("Density")

    #plt.title(title, fontsize=12)
    #subtitle = r'Histogram of {0}: $\mu={1}$, $\sigma={2}$'.format(categoryName, mu,  sigma)
    subtitle = r'Histogram of {0}'.format(categoryName)
    plt.suptitle(subtitle, fontsize=12)

    # save plot
    plt.savefig(filename, bbox_inches='tight')
    plt.gcf().clear()
    plt.cla()
    plt.clf()
    plt.close()


def plotTemplateDistribution(categoryName, templates, filepath):

    filename = filepath + '/templates-distribution-' + categoryName + '.png'

    x_ticks = np.arange(1, templates.shape[0] + 1, 1)
    plt.xticks(x_ticks, templates.index.values, rotation='vertical')

    y = templates["Count"] / float(templates['Count'].sum())

    plt.ylabel("Distribution")
    plt.xlabel("Templates")

    plt.grid(linestyle='dotted', alpha=0.5)
    plt.scatter( x_ticks, y, s=30, alpha=0.9)

    plt.savefig(filename, bbox_inches='tight')

    plt.gcf().clear()
    plt.cla()
    plt.clf()
    plt.close()


def plotCategoriesTemplatesDistribution(templatesDistributions, filepath):
    data = []
    i = 1
    for element in templatesDistributions:
        color = plt.cm.tab20(i)
        colorl = list(color)
        colorl[3] = 0.5
        color = tuple(colorl)

        for tupla in element:
            x, labels, y = tupla
            data.append(dict(categoryN=i, category=x, distribution=y,
                             infobox_template=labels, c=color))
        i += 1

    df = pd.DataFrame(data)

    groups = df.groupby('categoryN')

    names =[]
    for name, group in groups:
        names.append(group.category.values[0])

    fig, ax = plt.subplots(figsize=(22, 10))

    groups.plot(x='categoryN', y='distribution', kind='scatter',
                s=1, xlim=(-1.5, 22), ax=ax, colorbar=False)

    for name, group in groups:
        a = pd.concat({'c':group.c, 'categoryN': group.categoryN,
                       'distribution': group.distribution,
                       'infobox_template': group.infobox_template}, axis=1)
        for i, point in a.iterrows():
            ax.text(point['categoryN'], point['distribution'],
                    str(point['infobox_template']), ha='center',
                    va='center', fontsize='x-large', backgroundcolor=point['c'], weight='bold')

    x_ticks = np.arange(1, len(names) + 1, 1)
    plt.xticks(x_ticks, names, rotation='vertical', fontsize=18)
    plt.yticks(fontsize=18)
    plt.ylabel("")
    plt.xlabel("")
    plt.grid(color='grey', linestyle='--', linewidth=0.8)
    plt.savefig(filepath, bbox_inches='tight')
    plt.gcf().clear()
    plt.cla()
    plt.clf()
    plt.close()

def plotBoxplot(categoriesSimilarities, filepath):
    categoriesName = []
    data_to_plot = []
    for index, category in enumerate(categoriesSimilarities):
        data_to_plot.append(category[1])
        categoriesName.append(category[0])

    fig = plt.figure(1, figsize=(9, 6))
    # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot
    bp = ax.boxplot(data_to_plot)
    ax.set_xticklabels(categoriesName, rotation=90)

    plt.title('Infoboxes homogeneity by category', fontsize=12)

    # save plot
    plt.savefig(filepath, bbox_inches='tight')
    plt.gcf().clear()
    plt.cla()
    plt.clf()
    plt.close()

def plotInfoboxesSizeBoxplot(categories, infoboxesSize, filepath):
    fig = plt.figure(1, figsize=(9, 6))
    # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot
    ax.boxplot(infoboxesSize)
    ax.set_xticklabels(categories, rotation=90)

    plt.title("Distribution of infoboxes size by category", fontsize=12)

    # save plot
    plt.savefig(filepath, bbox_inches='tight')
    plt.gcf().clear()
    plt.cla()
    plt.clf()
    plt.close()

def plotQualityBoxplot(categories, similarities, filepath):
    fig = plt.figure(1, figsize=(9, 6))
    # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot
    ax.boxplot(similarities)
    ax.set_xticklabels(categories, rotation=90)

    plt.title("Infoboxes similarity with community template", fontsize=12)

    # save plot
    plt.savefig(filepath, bbox_inches='tight')
    plt.gcf().clear()
    plt.cla()
    plt.clf()
    plt.close()

def plotPropsUsageBoxplot(categories, similarities, filepath):
    fig = plt.figure(1, figsize=(9, 6))
    # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot
    ax.boxplot(similarities)
    ax.set_xticklabels(categories, rotation=90)

    plt.title("Template properties usage", fontsize=12)

    # save plot
    plt.savefig(filepath, bbox_inches='tight')
    plt.gcf().clear()
    plt.cla()
    plt.clf()
    plt.close()

def groupPropsBarPlot(df, filepath, title):
    # identifies empty columns
    dfEmptyColumns = list(pd.isnull(df).sum() == df.shape[0])

    # Setting the positions and width for the bars
    pos = range(0, df.shape[0])

    width = 0.15

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(6, 10))

    colors = np.array(['#550080', '#8080ff', '#008000', '#ff00ff', '#b32400', '#392613', '#e60073'])

    if(len(dfEmptyColumns)==8):
        colors = np.append(colors, '#7d3c98')

    #removes empty columns for plot
    if dfEmptyColumns != 0:
        df = df.drop(df.columns[dfEmptyColumns], axis=1)
        colors = colors[~np.array(dfEmptyColumns)]
        labels = list(df.columns)
        del labels[0]

    dfAux = df.drop('Category', 1)
    i = 0
    for name, values in dfAux.iteritems():
        plt.barh([p + width*i for p in pos], values, width, alpha=0.8, color=colors[i], label=name)
        i += 1

    # Set the chart's title
    plt.title(title)

    # Set the y axis label
    ax.set_xlabel('Proportion')

    # Set the position of the x ticks
    ax.set_yticks([p + 2 * width for p in pos])

    # Set the labels for the x ticks
    ax.set_yticklabels(df['Category'], fontsize=12)

    # Adding the legend and showing the plot
    plt.legend(labels, loc='upper right')
    plt.grid(linestyle='dashed')
    plt.tight_layout()

    # save plot
    plt.savefig(filepath)
    plt.gcf().clear()
    plt.cla()
    plt.clf()
    plt.close()


