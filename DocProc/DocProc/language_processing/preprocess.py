# Contains various language related operations
# Its dependency are spacywrapper.py and nltk

import re
from stemming.porter2 import stem
from nltk import corpus
from .spacywrapper import SWrapper
from nltk.tokenize import RegexpTokenizer
from .contractions import expandContractions
from nltk.tokenize import sent_tokenize, word_tokenize

# Logger
import logging
logger = logging.getLogger(__name__)

# Global variables
Stopwords = list()
alphanum_tokenizer = RegexpTokenizer(r'\w+')

def preprocessing(document, type='basic', asci=True, lowercase=True,
					stopwords=True, stopword_list=list(), alpha_num=True, 
					contraction=True, stemming=False, lemmatize=False, 
					pos_patterns=False, nums=True):
	'''
	Delegates preprocessing implementation
	'''
	global Stopwords
	Stopwords = list(corpus.stopwords.words('english'))

	# Cleansing off certain symbols, before preprocessing
	document = cleansing(document)

	# Adding new stop words to list
	if stopword_list:
		Stopwords.extend(stopword_list)

	if type == 'basic':
		return basic_preprocessing(document, asci=asci, lowercase=lowercase, 
									stopwords=stopwords, alpha_num=alpha_num, 
									contraction=contraction, stemming=stemming, 
									nums=nums)

	elif type == 'advance':
		return advance_preprocessing(document, asci=asci, lowercase=lowercase, 
										stopwords=stopwords, 
										alpha_num=alpha_num, 
										contraction=contraction, 
										stemming=stemming, lemmatize=lemmatize,
										pos_patterns=pos_patterns)

	else:
		logger.warning('Invalid Preprocessing Choice')
		sys.exit(0)

def cleansing(document):
	'''
	Hardcoded symbol removal/replacement, bad code 
	1. Removes escape characters
	2. Removes certain symbols
	3. Replaces certain symbols
	'''

	# Removing all escape characters
	# Removing forbidden items
	forbidden_list = ["'s"]
	for x in forbidden_list:
		if x in document:
			document = document.replace(x,'')

	# Replace items(keys) with their respective values
	replace_dict = {"_":" ","-":" "}
	for rep, equi in replace_dict.items():
		if rep in document:
			document = document.replace(rep, equi)

	return document

def basic_preprocessing(document, asci=True, lowercase=True, stopwords=True, 
						alpha_num=True, contraction=True, stemming=False, 
						nums=True):
	'''
	Performs the following operations and returns a cleansed document
	1. Reduces to lower case
	2. Expands contractions
	3. Removes non-alphanum
	4. Removes stop words
	5. Stemming of words
	6. Removes numbers as strings
	'''

	tokens = list()

	# Remove non-ascii
	if asci: 
		document = ''.join([i for i in document if ord(i) < 128])

	# Clear unwanted spaces
	document = document.strip()

	# Reduce to lower case
	if lowercase:
		document = document.lower()

	# removing extra space
	document = re.sub(' +', ' ', document)

	# removing escape characters
	document = document.replace('\\','\\\\').replace('"','\\"')

	# removing web links
	document = re.sub(r'https\S+', '', document)

	# Expanding contractions. Minimalistic implementation
	if contraction:
		document = expandContractions(document)

	# Removing non-alphanums
	if alpha_num:
		tokens = alphanum_tokenizer.tokenize(document)
	else:
		# Simple tokenization
		tokens = word_tokenize(document)

	# Removing single length tokens, covering shortcoming of tokenization
	tokens = [x for x in tokens if len(x) > 2]

	# Removing stopwords
	if stopwords:
		tokens = [x for x in tokens if x not in Stopwords]

	# Stemming
	if stemming:
		tokens = [stem(x) for x in tokens]

	# Removing numbers
	if not nums:
		tokens = [x for x in tokens if not x.isnumeric()]
		
	# Accumulating tokens back into document
	document = ' '.join(tokens)
	
	return document 

def advance_preprocessing(document, asci=True, lowercase=True, stopwords=True,
						 alpha_num=True, contraction=True, stemming=False,
						 lemmatize=False, pos_patterns=list()):
	'''
	Performs the following operations and returns a cleansed document
	1. Basic preprocessing + Lemmatization
	'''
	# Delegating after instance creation to preserve sentence

	if lemmatize or pos_patterns:
		cleansed_words = list()

		# Disabling various components of spacy for faster loading
		disable = list()
		if pos_patterns:
			disable = ['ner','parser']
		else:
			disable = ['ner','parser','tagger']

		# Sentence tokenization for spacy instance creation
		spacy_obj = SWrapper(disable=disable)
		sentences = sent_tokenize(document)

		for inp_sent in sentences:
			# To make lemmatization better, convert to lower case
			spacy_obj.set_sent(inp_sent)

			# Accumulating words
			if pos_patterns:
				# Extracting only pos_patterns
				tokens = spacy_obj.get_some_tags(patterns=pos_patterns)

				if lemmatize:
					# Lemmatization after noun extraction, so update sentence
					spacy_obj.set_sent(' '.join(tokens))

				else:
					# Without lemmatization, just appended pos_patterns
					cleansed_words.extend(tokens)

			# lemmatization, excluding propos_patterns
			if lemmatize:
				cleansed_words.extend([x[1] for x in spacy_obj.get_lemmas() 
										if x[1] != '~PRON~'])

		# Accumulating document
		document = ' '.join(cleansed_words) 

	# Delegating basic preprocessing
	document = basic_preprocessing(document, asci=asci, lowercase=lowercase, 
									stopwords=stopwords, alpha_num=alpha_num, 
									contraction=contraction, stemming=stemming)

	return document

if __name__ == '__main__':
	inp_sent = input('Enter Input Sentence for Preprocessing : \n >> ')

	print ('Basic Preprocessing : ',preprocessing(inp_sent, type='basic'))
	print ('Advance Preprocessing : ',preprocessing(inp_sent, type='advance'))
	