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
categoriesMeanTemplatePropsUsage = []
categoriesTemplatePropsUsage = []
categoriesTemplatePropsMissUsage = []
categoriesPropsMissUsage = []
mappedInfoboxTemplateProportion = []

# Read datasets
categoriesName = inp.readFiles(constants.infobox_datasets)

for categoryName in categoriesName:
    categoryName = categoryName.replace(".csv","")
    categories.append(categoryName)

    # get category infobox dataset as articles
    articles = csv.readCSVFile(constants.infobox_datasets+"/"+categoryName+".csv")

    articlesWithInfobox = stat.getArticlesWithInfoboxScheme(articles)

    articlesWithTemplate = csv.readCSVFile(constants.article_template_datasets+"/"+categoryName+".csv")

    templatesParameters = csv.readCSVFile(constants.template_datasets+"/"+categoryName+".csv")

    catMappedInfoboxes = articlesWithInfobox.shape[0]
    catMappedTemplates = articlesWithTemplate.shape[0]

    print("=================== %s ====================" % categoryName)

    if catMappedInfoboxes == 0:
        infoboxTemplateProportion = 0.0
    else:
        infoboxTemplateProportion = float(catMappedInfoboxes) / float(catMappedTemplates)
        mappedInfoboxTemplateProportion.append([categoryName, infoboxTemplateProportion])
        infoboxNoTemplate = articlesWithInfobox[~np.isin(articlesWithInfobox[:, 0], articlesWithTemplate[:, 0]), 0]
        print("Infobox mapping, missing template: %s " % infoboxNoTemplate)
        templateNoInfobox = articlesWithTemplate[~np.isin(articlesWithTemplate[:, 0], articlesWithInfobox[:, 0]), 0]
        print("Template mapping, missing infobox: %s " % templateNoInfobox)

    print("Generating infobox distribution per category")

    if(articlesWithTemplate.shape[0] > 0):
        unique, counts = np.unique(articlesWithTemplate[:,1], return_counts=True)
        templatesDist = pd.DataFrame(counts, columns=["Count"], index=unique)
        sortedTemplatesDistribution = templatesDist.sort_values(by="Count", axis=0, ascending=False)
        v.plotTemplateDistribution(categoryName, sortedTemplatesDistribution, 'results/plots/template')

        sortedTemplatesDistribution['Count'] = sortedTemplatesDistribution['Count'] / float(sortedTemplatesDistribution['Count'].sum())

        sortedTemplatesDistribution['Template'] = sortedTemplatesDistribution.index
        templateCSV = pd.DataFrame(sortedTemplatesDistribution)
        templateCSV.to_csv("results/csv/templates/"+categoryName+"-distribution.csv", index=False, header=True, sep=",")

        infoboxSimilarities = quality.calculatesInfoboxQuality(articlesWithInfobox, articlesWithTemplate, templatesParameters)
        similarities.append(infoboxSimilarities)

        meanTemplatePropsMissUsage, proportionsTemplatePropsMissUsage = quality.measuresTemplatePropsMissUsage(
            articlesWithInfobox, articlesWithTemplate, templatesParameters)
        print("MEAN PROPORTION NOT USED TEMPLATE PROPS %s " % meanTemplatePropsMissUsage)

        meanTemplatePropsUsage, proportionsTemplatePropsUsage = quality.measuresTemplatePropsUsage(
            articlesWithInfobox, articlesWithTemplate, templatesParameters)
        print("MEAN PROPORTION USED TEMPLATE PROPS %s " % meanTemplatePropsUsage)
        categoriesMeanTemplatePropsUsage.append({"Category": categoryName,
                                                 "Props usage": meanTemplatePropsUsage,
                                                 "Miss usage": meanTemplatePropsMissUsage})


        categoriesTemplatePropsMissUsage.append(proportionsTemplatePropsMissUsage)
        categoriesTemplatePropsUsage.append(proportionsTemplatePropsUsage)

        # count category elements
        articles_count, infoboxes_count, common_props_count = stat.countElements(articles)

        # calculates infobox properties miss usage
        propertiesProportion = stat.propertiesProportion(articles, infoboxes_count)
        props_missing_usage = stat.getMissingUsage(propertiesProportion)
        categoriesPropsMissUsage.append(props_missing_usage)

# prints CSV of measures for template props usage
categoriesMeanTemplatePropsUsage = pd.DataFrame(categoriesMeanTemplatePropsUsage)
categoriesMeanTemplatePropsUsage.to_csv('results/csv/wikipedia-template-props-usage.csv',
                                        index=False, header=True, sep=",")

# plot boxplots for properties miss usage
v.plotPropsMissUsageBoxplot(categories, categoriesPropsMissUsage,
                            "results/plots/quality/infobox-miss-props-usage-quality-all.png")

# plot boxplots for template properties usage
v.plotPropsUsageBoxplot(categories, categoriesTemplatePropsUsage,
                        "results/plots/quality/template-props-usage-quality-all.png",
                        title="Template properties usage")

# plot boxplots for template properties usage
v.plotPropsUsageBoxplot(categories, categoriesTemplatePropsMissUsage,
                        "results/plots/quality/template-props-miss-usage-quality-all.png",
                        title="Template properties miss usage")

# plot boxplots for infobox quality based on wikipedia templates
v.plotQualityBoxplot(categories, similarities, "results/plots/quality/infoboxes-quality-all.png")

# plot templates distributions for all categories
#v.plotCategoriesTemplatesDistribution(templates, 'results/plots/template/templates-dist-all.png')

print("Template-infobox proportions")
v.plotMappedInfoboxTemplateProportion(mappedInfoboxTemplateProportion,'results/plots/quality/infobox-template-mapping.png')

print("Finish plotting")

