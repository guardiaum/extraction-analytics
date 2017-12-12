import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getSimilarityWithTemplate(templatesParameters, template, article, infobox):
	cosine = 0;
	for temp in range(0, templatesParameters.shape[0]):
			
			if(templatesParameters[temp][0]==template):
				
				wikipediaTemplate = templatesParameters[temp][1:]
				
				tfidf = TfidfVectorizer(lowercase=True)
				docs = np.array([])
				
				if(wikipediaTemplate!=False and article!=False):
					docs = np.append(docs, np.array2string(np.array(infobox), separator=','))
					docs = np.append(docs, np.array2string(np.array(wikipediaTemplate), separator=',').replace("_", ""))
					
					#print("DBPEDIA INFOBOX ==============================================================")
					#print(infobox)
					#print("WIKIPEDIA INFOBOX template ===================================================")
					#print(wikipediaTemplate)
					
				representation = tfidf.fit_transform(docs)
				
				cosine = cosine_similarity(representation[0:1], representation)[0, 1]
				#print("Similarity: %s" % cosine)
				break;
	return cosine

def calculatesInfoboxQuality(articlesWithInfobox, articlesWithTemplate, templatesParameters):
	similarities = []
	
	rows, cols = articlesWithTemplate.shape
	
	# for each article selects its title and related template
	for row in range(0, rows):
		article = articlesWithTemplate[row, 0]
		template = articlesWithTemplate[row, 1]
		
		# selects article infobox and its related properties
		articleInfobox = np.where(articlesWithInfobox[:,0]==article)
		infoboxProps = articlesWithInfobox[articleInfobox,1:]
		# flatten array
		infobox = infoboxProps.flatten()
		# removes empty cells
		removeEmpty = np.where(infobox==' ')
		infobox = np.delete(infobox, removeEmpty)
		
		# iterates over templates dataset till find the one related with current article
		cosine = getSimilarityWithTemplate(templatesParameters, template, article, infobox)
		
		similarities.append(cosine)
	return similarities
	'''	
	quality = np.around(np.mean(np.array(similarities)), decimals=5)
	std_quality = np.around(np.std(np.array(similarities)), decimals=5)
	median_quality = np.around(np.median(np.array(similarities)), decimals=5)
	variance_quality = np.around(np.var(np.array(similarities)), decimals=5)
	
	print("Quality: %s" % quality)
	print("std_qualiity: %s" % std_quality)
	print("median_quality: %s" % median_quality)
	print("variance_quality %s" % variance_quality)
	'''
	
