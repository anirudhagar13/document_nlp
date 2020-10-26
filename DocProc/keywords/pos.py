# Implementing abstract class
import re
import json
from collections import Counter
from nltk.tokenize import sent_tokenize
from django.contrib.staticfiles import finders

from .abstract import Extractor
from .rake_algo import load_stop_words
from DocProc import SWrapper, preprocessing

# Logger
import logging
logger = logging.getLogger(__name__)

class POSExtractor(Extractor):
	def __init__(self, threshold=0.02):
		self._spacy = SWrapper(disable=['ner','parser'])
		self._threshold = threshold

	def get_keywords(self, text=''):
		# overwriting instance variable
		if not text:
			logger.warning('Empty `text` sent')
			raise Exception('Invalid parameter type sent')

		# Stopwords elimination
		path = finders.find('SmartStoplist.txt')
		stopwords = load_stop_words(path)

		# keyword extraction
		nouns = list()
		bigrams = dict()
		unigrams = dict()
		sentences = sent_tokenize(text)
		for sentence in sentences:
			
			# tokenizing sentence for parsing
			self._spacy.set_sent(sentence)
			nouns.extend(x.lower() 
						for x in self._spacy.get_some_tags(patterns=['NN']))

			# getting preprocessing done for popularity extraction
			cleansed_unigrams = preprocessing(sentence, type='basic', 
											asci=True, nums=False,
											stopword_list=stopwords).split()
			cleansed_bigrams = self._ngram_generation(cleansed_unigrams, 2)

			# getting only those bigrams which have atleast one noun
			cleansed_bigrams = [x for x in cleansed_bigrams 
								if x.split()[0] in nouns
								and x.split()[1] in nouns]

			# Hashing unigram
			for gram in cleansed_unigrams:
				if gram not in unigrams:
					unigrams[gram] = 0

				unigrams[gram] += 1

			# Hashing bigram
			for gram in cleansed_bigrams:
				if gram not in bigrams:
					bigrams[gram] = 0

				bigrams[gram] += 1

		# removing duplication across document
		nouns = list(set(nouns))

		# Manual stemming
		nouns = [x for x in nouns if x[-1] == 's' and x[:-1] not in nouns]

		# Preprocessing for frequency based extraction
		k_bi = int(len(bigrams)*self._threshold)
		k_uni = int(len(unigrams)*self._threshold)
		pop_bigrams = [x[0] for x in Counter(bigrams).most_common(k_bi)]
		pop_unigrams = [x[0] for x in Counter(unigrams).most_common(k_uni)]

		# Filter only popular nouns
		# print ('Before filtering nouns: ', len(nouns))
		# nouns = [x for x in nouns if x in pop_unigrams]
		# print ('After filtering nouns: ', len(nouns))

		return [pop_unigrams+pop_bigrams]

	def _ngram_generation(self, tokens, n):
		'''
		generate ngrams
		'''
		ngrams = zip(*[tokens[i:] for i in range(n)])
		return [" ".join(ngram) for ngram in ngrams]

	def __str__(self):
		'''
        To make instance printable
        '''
		return ('POS Based Keyword Extraction')

if __name__ == '__main__':
	pos = POSExtractor()
	a = pos.get_keywords("This is a test String. Test String it is.")
	print (a)
