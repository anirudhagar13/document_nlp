from .rake import RakeWrapper
from .pos import POSExtractor

# Logger
import logging
logger = logging.getLogger(__name__)

def extractFactory(extractor='rake'):
	'''
	Factory design pattern for keyword extraction
	'''
	if extractor == 'rake':
		return RakeWrapper()

	elif extractor == 'pos':
		return POSExtractor()

	else:
		logger.warning('Wrong extractor type')
		raise Exception('Invalid parameter sent.')
