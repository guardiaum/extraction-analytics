import util.my_csv as csv
import util.constants as constants
import statistics.common as stat
import util.input as inp
import plotting.visualization as v
import numpy as np
import pandas as pd
import quality.common as quality
import sys


def saveInfoboxTemplateMapping(categoryName, articlesWithInfobox, catMappedInfoboxes,
                           articlesWithTemplate, catMappedTemplates, namesLength):
    if catMappedInfoboxes == 0:
        infoboxTemplateProportion = 0.0
    else:
        infoboxTemplateProportion = float(catMappedInfoboxes) / float(catMappedTemplates)

    infoboxNoTemplate = articlesWithInfobox[~np.isin(articlesWithInfobox[:, 0], articlesWithTemplate[:, 0]), 0]
    templateNoInfobox = articlesWithTemplate[~np.isin(articlesWithTemplate[:, 0], articlesWithInfobox[:, 0]), 0]

    print("Infobox mapping, missing template: %s " % infoboxNoTemplate)
    print("Template mapping, missing infobox: %s " % templateNoInfobox)

    # saves bigger infoboxes
    mappedInfoboxTemplateProportion = pd.DataFrame(infoboxTemplateProportion, columns=["infobox-template-proportion"],
                                   index=[categoryName])

    if (namesLength == 1):
        mappedInfoboxTemplateProportion.to_csv('results/csv/temp-mapped-inf-temp-prop.csv',
                                               mode='w', index=True, header=True, encoding='utf-8')
    else:
        with open('results/csv/temp-mapped-inf-temp-prop.csv', 'a') as f:
            mappedInfoboxTemplateProportion.to_csv(f, index=True, header=False, encoding='utf-8')


def plotMappedInfoboxTemplate():
    print("Plot template-infobox proportions")

    mappedInfoboxTemplateProportion = csv.readCSVFile('results/csv/temp-mapped-inf-temp-prop.csv')

    v.plotMappedInfoboxTemplateProportion(mappedInfoboxTemplateProportion[1:],
                                          'results/plots/quality/infobox-template-mapping.png')


def saveSimilarities(articlesWithInfobox, articlesWithTemplate, templatesParameters, categoryName, namesLength):
    infoboxSimilarities = quality.calculatesInfoboxQuality(articlesWithInfobox, articlesWithTemplate,
                                                           templatesParameters)

    similarities = pd.DataFrame([infoboxSimilarities], index=[categoryName])

    if(namesLength == 1):
        similarities.to_csv('results/csv/temp-similarities.csv', mode='w', index=True, header=False, encoding='utf-8')
    else:
        with open('results/csv/temp-similarities.csv', 'a') as f:
            similarities.to_csv(f, index=True, header=False, encoding='utf-8')


def plotSimilarities():
    print("Plot infobox quality based on template similarity")

    similaritiesCSV = csv.readCSVFile('results/csv/temp-similarities.csv')

    names = []
    similarities = []
    for row in similaritiesCSV:
        names.append(row[0])
        similaritiesString = row[1:]
        similarities.append(map(float, similaritiesString))

    # plot boxplots for infobox quality based on wikipedia templates
    v.plotQualityBoxplot(names, similarities, 'results/plots/quality/infoboxes-quality-all.png')


#[external] templates based
def saveTemplatePropsUsageToFile(categoryName, meanTemplatePropsUsage,
                                 proportionsTemplatePropsUsage, meanTemplatePropsMissUsage,
                                 proportionsTemplatePropsMissUsage, namesLength):

    categoriesMeanTemplatePropsUsage = pd.DataFrame({"Category": categoryName,
                                                     "Mean props usage": meanTemplatePropsUsage,
                                                     "Proportion usage": [str(proportionsTemplatePropsUsage).strip('[]')],
                                                     "Mean miss usage": meanTemplatePropsMissUsage,
                                                     "Proportion miss": [str(proportionsTemplatePropsMissUsage).strip('[]')]})

    # prints CSV of measures for template props usage
    if(namesLength == 1):
        categoriesMeanTemplatePropsUsage.to_csv('results/csv/wikipedia-template-props-usage.csv', mode='w',
                                            index=False, header=True, encoding='utf-8')
    else:
        with open('results/csv/wikipedia-template-props-usage.csv', 'a') as f:
            categoriesMeanTemplatePropsUsage.to_csv(f, index=False, header=False, encoding='utf-8')


# [external] templates based
def plotExternalPropertiesUsage():
    print("Plot external properties usage")

    categoriesPropertiesUsage = pd.read_csv('results/csv/wikipedia-template-props-usage.csv', header=0)

    names = categoriesPropertiesUsage['Category']
    templatePropsUsage = categoriesPropertiesUsage['Proportion usage']

    props = []
    for row in templatePropsUsage:
        row = [float(item) for item in row.replace(' ','').split(',')]
        props.append(row)

    # plot boxplots for template properties usage
    v.plotPropsUsageBoxplot(names, props,
                            "results/plots/quality/template-props-usage-quality-all.png",
                            title="Template properties usage")


# [external] templates based
def plotExternalPropertiesMissUsage():
    print("Plot external properties miss usage")

    categoriesPropertiesUsage = pd.read_csv('results/csv/wikipedia-template-props-usage.csv', header=0)

    names = categoriesPropertiesUsage['Category']
    templatePropsMissUsage = categoriesPropertiesUsage['Proportion miss']

    props = []
    for row in templatePropsMissUsage:
        row = [float(item) for item in row.replace(' ', '').split(',')]
        props.append(row)

    # plot boxplots for template properties usage
    v.plotPropsUsageBoxplot(names, props,
                            "results/plots/quality/template-props-miss-usage-quality-all.png",
                            title="Template properties miss usage")


# [internal] category based
def savePropertiesProportionToFile(categoryName, articles, nameLength):
    # count category elements
    articles_count, infoboxes_count, common_props_count = stat.countElements(articles)

    # calculates infobox properties miss usage
    propertiesProportion = stat.propertiesProportion(articles, infoboxes_count)
    props_missing_usage = stat.getMissingUsage(propertiesProportion)

    categoriesPropsMissUsage = pd.DataFrame([props_missing_usage.values], index=[categoryName])

    if(nameLength == 1):
        categoriesPropsMissUsage.to_csv('results/csv/temp-internal-props-usage.csv', mode='w',
                                            index=True, header=False, encoding='utf-8')
    else:
        categoriesPropsMissUsage.to_csv('results/csv/temp-internal-props-usage.csv', mode='a',
                                        index=True, header=False, encoding='utf-8')


# [internal] category based
def plotInternalPropertiesMissUsage():
    print("Plot internal properties miss usage")
    names = []
    categoriesPropsMissUsage = []

    propsMissUsage = csv.readCSVFile('results/csv/temp-internal-props-usage.csv')
    for row in propsMissUsage:
        names.append(row[0])
        categoriesPropsMissUsage.append(map(float,row[1:]))

    # plot boxplots for properties miss usage
    v.plotPropsMissUsageBoxplot(names, categoriesPropsMissUsage,
                                "results/plots/quality/infobox-miss-props-usage-quality-all.png")


def run(args):
    # Read datasets
    categoriesName = inp.readFiles(constants.infobox_datasets)

    if len(args)==3:
        numberOfChunks = int(args[1])
        chunk2select = int(args[2]) - 1

        chunks = inp.chunkIt(categoriesName, numberOfChunks)

        categoriesName = chunks[chunk2select]

        print(chunks)
        print(categoriesName)

    names = []
    for categoryName in categoriesName:

        categoryName = categoryName.replace(".csv","")

        names.append(categoryName)

        print("=================== %s ====================" % categoryName)

        # get category infobox dataset as articles
        articles = csv.readCSVFile(constants.infobox_datasets+"/"+categoryName+".csv")

        savePropertiesProportionToFile(categoryName, articles, len(names))

        articlesWithInfobox = stat.getArticlesWithInfoboxScheme(articles)

        articlesWithTemplate = csv.readCSVFile(constants.article_template_datasets+"/"+categoryName+".csv")
        # normalize template mappings
        lowercased = np.char.lower(articlesWithTemplate[:, 1])
        articlesWithTemplate[:, 1] = lowercased

        tempParameters = csv.readCSVFile(constants.template_datasets+"/"+categoryName+".csv")

        # normalize template names
        templatesParameters = []
        for t in range(0, tempParameters.shape[0]):
            template_name = tempParameters[t][0].lower()
            wikipediaTemplate = tempParameters[t][1:]

            temp = [template_name]
            for i in range(len(wikipediaTemplate)):
                temp.append(wikipediaTemplate[i])
            templatesParameters.append(temp)

        templatesParameters = np.array(templatesParameters)

        catMappedInfoboxes = articlesWithInfobox.shape[0]

        catMappedTemplates = articlesWithTemplate.shape[0]

        saveInfoboxTemplateMapping(categoryName, articlesWithInfobox, catMappedInfoboxes,
                               articlesWithTemplate, catMappedTemplates, len(names))

        print("Generating infobox distribution per category")

        if(articlesWithTemplate.shape[0] > 0):

            saveSimilarities(articlesWithInfobox, articlesWithTemplate, templatesParameters, categoryName, len(names))

            sortedTemplatesDistribution = getTemplateDistributionSorted(articlesWithTemplate)

            plotAndSaveTemplateDistribution(categoryName, sortedTemplatesDistribution)

            meanTemplatePropsMissUsage, meanTemplatePropsUsage, proportionsTemplatePropsMissUsage, proportionsTemplatePropsUsage = getTemplatePropsMeasures(
                articlesWithInfobox, articlesWithTemplate, templatesParameters)

            saveTemplatePropsUsageToFile(categoryName,
                                         meanTemplatePropsUsage, proportionsTemplatePropsUsage,
                                         meanTemplatePropsMissUsage, proportionsTemplatePropsMissUsage,
                                         len(names))


def getTemplatePropsMeasures(articlesWithInfobox, articlesWithTemplate, templatesParameters):
    meanTemplatePropsMissUsage, proportionsTemplatePropsMissUsage = quality.measuresTemplatePropsMissUsage(
        articlesWithInfobox, articlesWithTemplate, templatesParameters)
    print("MEAN PROPORTION NOT USED TEMPLATE PROPS %s " % meanTemplatePropsMissUsage)
    meanTemplatePropsUsage, proportionsTemplatePropsUsage = quality.measuresTemplatePropsUsage(
        articlesWithInfobox, articlesWithTemplate, templatesParameters)
    print("MEAN PROPORTION USED TEMPLATE PROPS %s " % meanTemplatePropsUsage)
    return meanTemplatePropsMissUsage, meanTemplatePropsUsage, proportionsTemplatePropsMissUsage, proportionsTemplatePropsUsage


def plotAndSaveTemplateDistribution(categoryName, sortedTemplatesDistribution):
    v.plotTemplateDistribution(categoryName, sortedTemplatesDistribution, 'results/plots/template')
    sortedTemplatesDistribution['Count'] = sortedTemplatesDistribution['Count'] / float(
        sortedTemplatesDistribution['Count'].sum())
    sortedTemplatesDistribution['Template'] = sortedTemplatesDistribution.index
    templateCSV = pd.DataFrame(sortedTemplatesDistribution)
    templateCSV.to_csv("results/csv/templates/" + categoryName + "-distribution.csv", index=False, header=True, sep=",")


def getTemplateDistributionSorted(articlesWithTemplate):
    unique, counts = np.unique(articlesWithTemplate[:, 1], return_counts=True)
    templatesDist = pd.DataFrame(counts, columns=["Count"], index=unique)
    sortedTemplatesDistribution = templatesDist.sort_values(by="Count", axis=0, ascending=False)
    return sortedTemplatesDistribution


run(sys.argv)
plotMappedInfoboxTemplate()
plotSimilarities()
plotExternalPropertiesUsage()
plotExternalPropertiesMissUsage()
plotInternalPropertiesMissUsage()

print("Finish plotting")