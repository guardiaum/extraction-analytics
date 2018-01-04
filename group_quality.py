import util.my_csv as csv
import util.constants as constants
import statistics.common as stat
import util.input as inp
import plotting.visualization as v
import numpy as np
import pandas as pd
from astropy.stats import median_absolute_deviation
import quality.common as quality

categories = []
similarities = []
templates = []
measuresTemplatePropsUsage = []

# Read datasets
categoriesName = inp.readFiles(constants.infobox_datasets)

for categoryName in categoriesName:
    categoryName = categoryName.replace(".csv","")
    categories.append(categoryName)

    articles = csv.readCSVFile(constants.infobox_datasets+"/"+categoryName+".csv")

    articlesWithInfobox = stat.getArticlesWithInfoboxScheme(articles)

    articlesWithTemplate = csv.readCSVFile(constants.article_template_datasets+"/"+categoryName+".csv")

    templatesParameters = csv.readCSVFile(constants.template_datasets+"/"+categoryName+".csv")

    print("=================== %s ====================" % categoryName)
    
    print("Mapped infoboxes: %s" % articlesWithInfobox.shape[0])
    print("Mapped template: %s" %  articlesWithTemplate.shape[0])
    print("Infobox mapping, missing template: %s " %
          articlesWithInfobox[~np.isin(articlesWithInfobox[:, 0], articlesWithTemplate[:,0]), 0])
    print("Template mapping, missing infobox: %s " %
          articlesWithTemplate[~np.isin(articlesWithTemplate[:, 0], articlesWithInfobox[:, 0]), 0])

    print("Generating infobox distribution per category")
    unique, counts = np.unique(articlesWithTemplate[:,1], return_counts=True)
    templatesDist = pd.DataFrame(counts, columns=["Count"], index=unique)
    sortedTemplatesDistribution = templatesDist.sort_values(by="Count", axis=0, ascending=False)
    v.plotTemplateDistribution(categoryName, sortedTemplatesDistribution, 'results/plots/template')

    sortedTemplatesDistribution['Count'] = sortedTemplatesDistribution['Count'] / float(sortedTemplatesDistribution['Count'].sum())

    topTemplates = sortedTemplatesDistribution[sortedTemplatesDistribution['Count'] >= 0.1]
    templates.append(zip([categoryName] * topTemplates.shape[0], topTemplates.index.values, topTemplates['Count'].values))

    print("Plot infobox quality...")
    infoboxSimilarities = quality.calculatesInfoboxQuality(articlesWithInfobox, articlesWithTemplate, templatesParameters)
    similarities.append(infoboxSimilarities)

    measureTemplatePropsUsage = quality.measuresTemplatePropsUsage(articlesWithInfobox, articlesWithTemplate, templatesParameters)
    print("MEAN PROPORTION USED TEMPLATE PROPS %s " % measureTemplatePropsUsage)
    measuresTemplatePropsUsage.append({"Category": categoryName, "Props usage":measureTemplatePropsUsage})


# prints CSV os measures for template props usage
measuresTemplatePropsUsage = pd.DataFrame(measuresTemplatePropsUsage)
measuresTemplatePropsUsage.to_csv('results/csv/wikipedia-template-props-usage.csv', index=False, header=True, sep=",")

# plot templates distributions for all categories
v.plotCategoriesTemplatesDistribution(templates, 'results/plots/template/category-templates-dist-all.png')

# plot boxplots for infobox quality based on wikipedia templates
v.plotQualityBoxplot(categories, similarities, "results/plots/quality/category-infoboxes-quality-all.png")
print("Finish plotting")

