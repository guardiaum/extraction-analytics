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
                    docs = np.append(docs, np.array2string(np.array(infobox), separator=','))
                    # replace hifen (algumas propriedades do template aparecem com hifen)
                    docs = np.append(docs, np.array2string(np.array(wikipediaTemplate), separator=',')
                                     .replace("_", "").replace("-",""))

                representation = tfidf.fit_transform(docs)

                cosine = cosine_similarity(representation[0:1], representation)[0, 1]
                break;
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

def measuresTemplatePropsUsage(articlesWithInfobox, articlesWithTemplate, templatesParameters):
    proportions = []

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

        for templateParameters in templatesParameters:
            if templateParameters[0] == template_name:

                #print "TEMPLATE NAME", template_name
                templatePropsUsed, wikipediaTemplateSize = getTemplateInfoboxMeasure(templateParameters[1:], infobox)

                # proportion of template properties used by infobox over wikipedia template size
                proportions.append(templatePropsUsed / float(wikipediaTemplateSize))

    proportions = np.array(proportions) # proportions mean
    return np.mean(proportions), proportions

def getTemplateInfoboxMeasure(templateParameters, infobox):

    # normalize template parameters
    templateParameters = np.core.defchararray.replace(templateParameters, "_", "")
    templateParameters = np.core.defchararray.replace(templateParameters, "-", "")
    templateParameters = np.core.defchararray.lower(templateParameters)

    # normalize infobox parameters
    infoboxParameters = np.core.defchararray.lower(infobox)

    #print "INFOBOX"
    #print infoboxParameters
    #print "TEMPLATE"
    #print templateParameters

    intersec = np.intersect1d(infoboxParameters, templateParameters)
    used = intersec.shape[0]
    templateSize = templateParameters.shape[0]

    return used, templateSize