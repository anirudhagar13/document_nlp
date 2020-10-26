# Wrapper class for various embeddings
import sys 
import gensim
import gensim.downloader as api
from multiprocessing import cpu_count
from nltk.tokenize import sent_tokenize

# Logger
import logging
logger = logging.getLogger(__name__)

class WVWrapper():
	def __init__(self, model_path='', embedding_data='', 
					embedding_params=dict()):

		# Loading older model if exists
		embedding_inst = dict()

		# Data has to be lists of list
		if isinstance(embedding_data, str):
			# Converting para into list of sentences
			logger.info('Converting data into list of sentences')
			embedding_data = sent_tokenize(embedding_data)

		if isinstance(embedding_data, list):
			# Converting list of sentences into list of list of words
			logger.info('Converting data into list of list of words')
			embedding_data = [sent.split() for sent in embedding_data]

		# Abstracts loading, retraining and saving word2vec model
		try:
			# Loading word2vec using path
			embedding_inst = (gensim.models.Word2Vec.load(model_path))
			logger.info('Loading pre-trianed Word2Vec model')

			if embedding_data:
				# Update & save model. Data for training should be list of lists
				logger.info('Updating Word2Vec model')

				# Hardcoded updation parameters
				update_params = {'total_examples':len(embedding_data), 
									'epochs':5}

				# Model updation
				embedding_inst.build_vocab(embedding_data, update=True)
				embedding_inst.train(embedding_data, **update_params)

				# Saving model
				logger.info('Saving updated Word2Vec model')
				embedding_inst.save(model_path)

		except Exception as e:
			# No model with token found
			logger.info('No previous Word2Vec found.')

			if embedding_data:
				# Train & save model. Data for training should be list of lists
				logger.info('Training new Word2Vec model')

				if not embedding_params:
					embedding_params = {'min_count':2, 'size':100, 
										'workers':cpu_count(), 'window':5}

				embedding_inst = gensim.models.Word2Vec(embedding_data,
														**embedding_params)
				
				# Saving model
				logger.info('Saving new Word2Vec model')
				embedding_inst.save(model_path)

		self._word2vec = embedding_inst

	def get_embedding(self):
		'''
		simply returns the instance of word2vec loaded / trained
		'''
		return self._word2vec

	def get_distance(self, sentence_1, sentence_2):
		'''
		gives a measure of vector distance between two sentences or words
		'''
		sentence_1 = sentence_1.strip().lower().split()
		sentence_2 = sentence_2.strip().lower().split()

		if len(sentence_1) == 1 and len(sentence_2) == 1:
			# Finding distance between just two words
			return self._word2vec.distance(sentence_1[0], sentence_2[0])

		return self._word2vec.wmdistance(sentence_1, sentence_2)

	def get_similiarty(self, word_1, word_2):
		'''
		gives a measure of similarity between words
		'''
		if word_1 and word_2:
			return self._word2vec.similarity(word_1, word_2)

		else:
			return 0

	def get_vector(self, word):
		'''
		gives vector representation of a word
		'''
		if word:
			return self._word2vec[word]

		else:
			return []

	def __str__(self):
		return 'Wrapper class for Word2Vec Embedding'



