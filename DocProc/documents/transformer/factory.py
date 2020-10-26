# Factory for vectorizer instance

import sys
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from .embedding import WVWrapper
from ..files import getAbspath
from .custom_vec import MeanEmbeddingVectorizer, TfidfEmbeddingVectorizer

# Logger
import logging
logger = logging.getLogger(__name__)

def vectorizerFactory(vectorizer='tfidf', vectorizer_params=dict(), 
						data=list(), token='XXXX'):
	'''
	Factory to delegate instance creation
	'''

	# Inner function to get word2vec embedding
	def getEmbedding():
		model_path = getAbspath() + ('transformer/models/' + token + '_vec.kv')
		wv_inst = WVWrapper(model_path, data)
		return wv_inst.get_embedding()

	# Initializations
	vectorizer_inst = object()

	# Delegation
	if vectorizer == 'count':
		# Using simple tfidf vectorizer
		vectorizer_inst = CountVectorizer(**vectorizer_params)

	elif vectorizer == 'tfidf':
		# Using simple tfidf vectorizer
		vectorizer_inst = TfidfVectorizer(**vectorizer_params)

	elif vectorizer == 'w2v_mean':
		# Calling meanembedding vectorizer
		embedding = getEmbedding()
		vectorizer_inst = MeanEmbeddingVectorizer(word2vec=embedding, 
							vectorizer_params=vectorizer_params)
		
	elif vectorizer == 'w2v_tfidf':
		# Calling tfidfembedding vectorizer
		embedding = getEmbedding()
		vectorizer_inst = TfidfEmbeddingVectorizer(word2vec=embedding, 
							vectorizer_params=vectorizer_params)
			
	else:
		logger.warning('Invalid Vectorizer Choice or Embedding missing !!')
		sys.exit(0)

	return vectorizer_inst

def dimensionFactory(reducer='pca', reducer_params=dict()):
	'''
	Performs dimensionality reduction on the data obtained
	'''

	# Initializations
	reducer_params = object()

	# Delegation
	if reducer == 'pca':
		reducer_inst = TruncatedSVD(0.95)
			
	else:
		logger.warning('Invalid Dimensionality reducer choice !!')
		sys.exit(0)

	return reducer_inst
