# Implementing abstract class
# from rake_nltk import Rake
from .rake_algo import Rake
from .abstract import Extractor
from nltk.tokenize import sent_tokenize
from DocProc import preprocessing
from django.contrib.staticfiles import finders

# Logger
import logging
logger = logging.getLogger(__name__)

class RakeWrapper(Extractor):
	def __init__(self, threshold=0.05):
		# With django server
		path = finders.find('SmartStoplist.txt')
		self._r = Rake(path,3,2,5)
		self._threshold = threshold

	def get_keywords(self, text=''):
		# overwriting instance variable
		if not text:
			logger.warning('Parameter `text` sent empty')
			raise Exception('Invalid parameter sent')

		# # keyword extraction (older implementation)
		# if isinstance(text, list):
		# 	self._r.extract_keywords_from_sentences(text)

		# elif isinstance(text, str):
		# 	self._r.extract_keywords_from_text(text)

		# else:
		# 	logger.warning('Invalid `text` type')
		# 	raise Exception('Invalid parameter sent')

		# # Ranking and giving back above threshold
		# phrases_with_scores = self._r.get_ranked_phrases_with_scores()
		# print ('Phrases Obtained')

		# k_bucket = list()
		# scores = list()
		# k = int(len(phrases_with_scores) * self._threshold)
		# for bundle in phrases_with_scores:
		# 	if len(k_bucket) < k:
		# 		k_bucket.append(bundle[1])
		# 		scores.append(bundle[0])

		# 	else:
		# 		if min(scores) < bundle[0]:
		# 			index = scores.index(min(scores))
		# 			del scores[index]
		# 			del k_bucket[index]
		# 			k_bucket.append(bundle[1])
		# 			scores.append(bundle[0])

		# keyword extraction (older implementation)
		# Running new instance of rake
		keywords = self._r.run(text)
		k_bucket = [x[0] for x in keywords]

		# return r.get_ranked_phrases_with_scores() 
		return k_bucket

	def __str__(self):
		'''
        To make instance printable
        '''
		return ('Rake Based Keyword Extraction')

if __name__ == '__main__':
	# Test class here
	pass
