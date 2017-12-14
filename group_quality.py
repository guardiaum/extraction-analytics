import util.my_csv as csv
import util.constants as constants
import statistics.common as stat
import util.input as inp
import plotting.visualization as v
import numpy as np
import pandas as pd
from astropy.stats import median_absolute_deviation
import quality.common as quality


categoriesLinkage = [] # Linkage vector for plot a group

# Read datasets
categoriesName, outputFileName, title, subtitle = inp.readGroupOfFiles(constants.infobox_datasets)

for categoryName in categoriesName:
    categoryName = categoryName.replace(".csv","")

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
    v.plotTemplateDistribution(categoryName, sortedTemplatesDistribution, 'results/plots/template/')

    print("Plot infobox quality...")
    similarities = quality.calculatesInfoboxQuality(articlesWithInfobox, articlesWithTemplate, templatesParameters)
    #similarities = median_absolute_deviation(similarities, axis=0)
    #print(similarities)
    v.plotQualityBoxplot(categoryName, similarities, "results/plots/quality/", "Infobox quality by category", categoryName)
    print("Finish plotting")

