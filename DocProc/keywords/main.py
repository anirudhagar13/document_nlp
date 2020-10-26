'''
Runs control flow of keyword extraction module
'''
from .extract_fact import extractFactory

# Logger
import logging
logger = logging.getLogger(__name__)

def keyword_extraction(data):
	'''
	gets keyword extractor instance and performs extraction
	'''
	extractor_inst = ''

	# Instance creation
	if 'extractor' in data and data['extractor']:
		extractor_inst = extractFactory(extractor=data['extractor'])

	else:
		logger.warning('Parameter absent `extractor`')
		raise Exception('Insufficient parameters provided.')

	# Setting threshold
	if 'threshold' in data and isinstance(data['threshold'],float):
		extractor_inst._threshold = data['threshold']

	# Keyword extraction
	logger.info('Keyword Extractor instance created')

	if 'text' in data and data['text']:
		return extractor_inst.get_keywords(data['text'])

	else:
		logger.warning('Parameter absent `text`')
		raise Exception('Insufficient parameters provided.')
