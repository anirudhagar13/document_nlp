import sys
import gensim
import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

# Implementing abstract class
from .abstract import Transformer

# Logger
import logging
logger = logging.getLogger(__name__)

class MeanEmbeddingVectorizer(Transformer):
    def __init__(self, word2vec=None, vectorizer_params=dict()):
        '''
        Constructor
        '''
        if not word2vec:
            logger.error('Please send word2vec to MeanEmbeddingVectorizer !')
            sys.exit(0)

        self._word2vec = word2vec
        self._vectorizer_params = vectorizer_params
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = word2vec.vector_size

    def fit(self, X, y=None):
        '''
        Nothing happens here
        '''
        logger.info("MeanEmbeddingVectorizer 'fit' module")
        return self

    def transform(self, X, y=None):
        '''
        Calculates mean of all word vectors in a document.
        Receives list of documents and need list of list of words
        '''
        logger.info("MeanEmbeddingVectorizer 'transform' module")
        return np.array(
                [np.mean(
                    [self._word2vec[word] for word in document.split() 
                    if word in self._word2vec]
                or [np.zeros(self.dim)], axis=0)
            for document in X
        ])

    def fit_transform(self, X, y=None):
        '''
        First fit then transform
        '''
        self.fit(X, y)
        return self.transform(X, y)

    def __str__(self):
        '''
        To make instance printable
        '''
        return ('MeanEmbedding Vectorizer')

class TfidfEmbeddingVectorizer(Transformer):
    def __init__(self, word2vec=None, vectorizer_params=dict()):
        '''
        Constructor
        '''
        if not word2vec:
            logger.info('Please send word2vec to TfidfEmbeddingVectorizer !')
            sys.exit(0)
            
        self._word2vec = word2vec
        self._vectorizer_params = vectorizer_params
        self.word_weights = None
        self.dim = word2vec.vector_size

    def fit(self, X, y=None):
        '''
        Fits a tfidf vectorizer and creates a default dict having tfidf weights
        for all words in the vocubalry
        '''
        logger.info("TfidfEmbeddingVectorizer 'fit' module")
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of 
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word_weights = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X, y=None):
        '''
        Multiple word vectors with tfidf and weights and get their mean for all 
        words in a document
        '''
        logger.info("TfidfEmbeddingVectorizer 'transform' module")
        return np.array(
                [np.mean(
                    [self._word2vec[word] * self.word_weights[word]
                    for word in document.split() if word in self._word2vec] 
                or [np.zeros(self.dim)], axis=0)
                for document in X
            ])

    def fit_transform(self, X, y=None):
        '''
        first fit then transform
        '''
        self.fit(X, y)
        return self.transform(X, y)

    def __str__(self):
        '''
        To make instance printable
        '''
        return ('TfidfEmbedding Vectorizer')
        