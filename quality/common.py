import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getSimilarityWithTemplate(templatesParameters, template_name, article, infobox):
    cosine = 0;

    # iterates over templates parameters from category
    for temp in range(0, templatesParameters.shape[0]):

            # compares if the first column from templates parameters corresponds to informed template name
            if templatesParameters[temp][0] == template_name:

                # gets all properties from wikipedia template
                wikipediaTemplate = templatesParameters[temp][1:]

                tfidf = TfidfVectorizer(lowercase=True)

                # creates doc with extracted infobox properties and properties from wikipedia template
                docs = np.array([])
                if wikipediaTemplate is not False and article is not False :
                    docs = np.append(docs, np.array2string(np.array(infobox), separator=',')
                                     .replace("_", "").replace("-",""))
                    # replace hifen (algumas propriedades do template aparecem com hifen)
                    docs = np.append(docs, np.array2string(np.array(wikipediaTemplate), separator=',')
                                     .replace("_", "").replace("-",""))

                representation = tfidf.fit_transform(docs)

                cosine = cosine_similarity(representation[0:1], representation)[0, 1]
                return cosine
    return cosine

def calculatesInfoboxQuality(articlesWithInfobox, articlesWithTemplate, templatesParameters):
    similarities = []

    rows, cols = articlesWithTemplate.shape

    # for each article selects its title and related template
    for row in range(0, rows):
        article = articlesWithTemplate[row, 0]
        template_name = articlesWithTemplate[row, 1]

        # selects article infobox and its related properties
        articleInfobox = np.where(articlesWithInfobox[:,0]==article)
        infoboxProps = articlesWithInfobox[articleInfobox,1:]
        # flatten array
        infobox = infoboxProps.flatten()
        # removes empty cells
        removeEmpty = np.where(infobox==' ')
        infobox = np.delete(infobox, removeEmpty)

        # iterates over templates dataset till find the one related with current article
        cosine = getSimilarityWithTemplate(templatesParameters, template_name, article, infobox)

        similarities.append(cosine)
    return similarities

# Calculates the proportion of template properties that are not used by recovered infoboxes
# Receives as parameters articles with infobox, articles with respective template names
#  and templates with its parameters
def measuresTemplatePropsMissUsage(articlesWithInfobox, articlesWithTemplate, templatesParameters):
    proportions = []

    rows, cols = articlesWithTemplate.shape

    # for each article selects its title and related template
    for row in range(0, rows):
        article_title = articlesWithTemplate[row, 0]
        template_name = articlesWithTemplate[row, 1]

        # selects article infobox and its related properties
        articleInfobox = np.where(articlesWithInfobox[:,0]==article_title)
        infoboxProps = articlesWithInfobox[articleInfobox, 1:]

        # flatten array
        infobox = infoboxProps.flatten()

        # removes empty cells
        removeEmpty = np.where(infobox==' ')
        infobox = np.delete(infobox, removeEmpty)

        # for each template in templatesParameters it searches for template
        # with the same name as the one mapped in the infobox
        for templateParameters in templatesParameters:

            if templateParameters[0] == template_name: # finds mapped template in infobox
                # gets the measure of not used template properties by the recovered infobox
                notUsedPropsMeasure = getNotUsedPropertiesMeasure(templateParameters[1:], infobox)

                # proportion of template properties not used by infobox over wikipedia template size
                proportions.append(notUsedPropsMeasure)

    # returns mean proportion and the proportion of miss usage in each article
    return np.mean(np.array(proportions)), proportions

# Calculates the proportion of template properties that are used by recovered infoboxes
# Receives as parameters articles with infobox, articles with respective template names
# and templates with its parameters
def measuresTemplatePropsUsage(articlesWithInfobox, articlesWithTemplate, templatesParameters):
    proportions = []
    templates_size = []

    rows, cols = articlesWithTemplate.shape

    # for each article selects its title and related template
    for row in range(0, rows):
        article = articlesWithTemplate[row, 0]
        template_name = articlesWithTemplate[row, 1]

        # selects article infobox and its related properties
        articleInfobox = np.where(articlesWithInfobox[:,0]==article)
        infoboxProps = articlesWithInfobox[articleInfobox,1:]
        # flatten array
        infobox = infoboxProps.flatten()
        # removes empty cells
        removeEmpty = np.where(infobox==' ')
        infobox = np.delete(infobox, removeEmpty)

        # for each template in templatesParameters it searches for template
        # with the same name as the one mapped in the infobox
        for templateParameters in templatesParameters:
            if templateParameters[0] == template_name:
                # gets the measure of used template properties by the recovered infobox
                usedPropsMeasure, template_size = getUsedPropertiesMeasure(templateParameters[1:], infobox)

                # proportion of template properties used by infobox over wikipedia template size
                proportions.append(usedPropsMeasure)
                templates_size.append(template_size)

    return np.mean(np.array(proportions)), proportions, templates_size

# finds the measure of not used template properties by the respective infobox
def getNotUsedPropertiesMeasure(templateParameters, infoboxParameters):

    infoboxParameters, templateParameters = normalizeTemplateInfoboxProperties(infoboxParameters, templateParameters)

    #gets the difference btw template and infobox parameters
    difference = np.setdiff1d(templateParameters, infoboxParameters)
    notUsed = difference.shape[0]
    templateSize = templateParameters.shape[0]

    return notUsed / float(templateSize) # returns proportion

# finds the measure of used template properties by the respective infobox
def getUsedPropertiesMeasure(templateParameters, infobox):

    infoboxParameters, templateParameters = normalizeTemplateInfoboxProperties(infobox, templateParameters)

    # gets the intersection btw template and infobox parameters
    intersec = np.intersect1d(infoboxParameters, templateParameters)
    used = intersec.shape[0]
    templateSize = templateParameters.shape[0]

    return used / float(templateSize), templateSize# returns proportion

# normalize template e recovered infobox parameters
def normalizeTemplateInfoboxProperties(infobox, templateParameters):
    # normalize template parameters
    templateParameters = np.core.defchararray.replace(templateParameters, "_", "")
    templateParameters = np.core.defchararray.replace(templateParameters, "-", "")
    templateParameters = np.core.defchararray.replace(templateParameters, " ", "")
    templateParameters = np.core.defchararray.lower(templateParameters)
    templateParameters = np.unique(templateParameters)

    # normalize infobox parameters
    infobox = np.core.defchararray.replace(infobox, "_", "")
    infobox = np.core.defchararray.replace(infobox, "-", "")
    infobox = np.core.defchararray.replace(infobox, " ", "")
    infobox = np.core.defchararray.lower(infobox)
    infobox = np.unique(infobox)

    return infobox, templateParameters