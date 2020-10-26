# SKlearn algorithms

import sys
import numpy as np
import pandas as pd
from sklearn.exceptions import NotFittedError

# Models
from sklearn.svm import SVC, LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from keras import layers
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasClassifier

# Implementing abstract class
from .abstract import Estimator

# Logger
import logging
logger = logging.getLogger(__name__)

class SKEstimator(Estimator):
	def __init__(self, estimator='svm', model_params=dict(),
				transformers=None, model_path=''):
		'''
		To initialize the sklearn pipeline.
		Transformers taken as parameter as pipeline implementation
		is specific to this class.
		'''
		model = list()
		self.pipeline_inst = object()
		self._estimator = estimator
		self._model_path = model_path
		self._model_params = model_params

		# Putting vectorizer and other transformers, if any
		if transformers:
			model.extend(transformers)

		# Initializing various classifiers
		if estimator == 'naive':
			model.append(('clf-naive', MultinomialNB()))

		elif estimator == 'svm':
			if not self._model_params:
				self._model_params = {'loss':'log', 'penalty':'l2',
									 'alpha':0.01, 'random_state':42,
									 'max_iter':100000,}

			model.append(('clf-svm', SGDClassifier(**self._model_params)))

		elif estimator == 'log':
			if not self._model_params:
				self._model_params = {}

			model.append(('clf-log', LogisticRegression(**self._model_params)))


		elif estimator == 'linearsvc':
			if not self._model_params:
				self._model_params = {'probability':True, 'kernel':'linear', 
								'max_iter':5000, 'random_state':42}

			# Does not contain predict_proba, so workaround
			# model.append(('clf-linearsvc', LinearSVC(**self._model_params)))
			model.append(('clf-linearsvc', SVC(**self._model_params)))

		elif estimator == 'svmsvc':
			if not self._model_params:
				self._model_params = {'probability':True, 'max_iter':5000,
									 'random_state':42}

			model.append(('clf-svmsvc', SVC(**self._model_params)))

		elif estimator == 'random':
			model.append(('clf-random', RandomForestClassifier()))

		elif estimator == 'bag':
			model.append(('clf-bag', BaggingClassifier()))

		elif estimator == 'gboost':
			model.append(('clf-gboost', GradientBoostingClassifier()))

		elif estimator == 'adaboost':
			model.append(('clf-gboost', AdaBoostClassifier()))

		elif estimator == 'deepnet':
			clf = KerasClassifier(build_fn=deep_model,verbose=0)
			model.append(('clf-deep', clf))

		else:
			logger.warning('Invalid SKlearn Estimator !')
			sys.exit(0)

		self.pipeline_inst = Pipeline(model)

	def fit(self, train_data, train_target):
		'''
		To fit model
		'''
		logger.info("SKEstimator 'fit' module")

		# Fitting
		self.pipeline_inst.fit(train_data, train_target)	

		# Save model using default implementation
		super().save_model(self.pipeline_inst, self._model_path, 
							self._estimator)

		return self.pipeline_inst

	def predict(self, test_data):
		'''
		To predict classes as per trained model
		'''
		logger.info("SKEstimator 'predict' module")
		predicted = object()
		
		try:
			# Making predictions
			predicted = self.pipeline_inst.predict(test_data)

		except NotFittedError as e:
			# Load previously saved model using default implementation
			self.pipeline_inst = super().load_model(self._model_path, 
													self._estimator)

			# Making predictions
			predicted = self.pipeline_inst.predict(test_data)		

		return predicted

	def predict_proba(self, test_data):
		'''
		To predict probabilities as per trained model
		'''
		logger.info("SKEstimator 'predict_proba' module")
		predicted = object()
		
		try:
			# Making predictions
			predicted = self.pipeline_inst.predict_proba(test_data)

		except NotFittedError as e:
			# Load previously saved model using default implementation
			self.pipeline_inst = super().load_model(self._model_path, 
													self._estimator)

			# Making predictions
			predicted = self.pipeline_inst.predict_proba(test_data)

		# Wrapping predictions
		df = pd.DataFrame(predicted, columns=self.pipeline_inst.classes_)

		return df

	def score(self, test_data, test_target):
		'''
		Evaluates models accuracy on test data
		'''
		predicted_values = np.array(self.predict(test_data))
		test_target = np.array(test_target)

		# Checking equality
		results = (predicted_values == test_target)

		# Matching both numpy arrays
		return sum(results) / len(results)

	def __str__(self):
		'''
		To make instance printable
		'''
		return ('SKEstimator Instance : ' + self._estimator +
				' Params : ' + self._model_params)

def deep_model(model_params=dict()):
	# create model
	model = Sequential()
	# model.add(layers.GlobalMaxPool1D())
	# model.add(layers.Flatten())
	model.add(layers.Dense(10, activation='relu'))
	model.add(layers.Dense(1, activation='sigmoid'))
	model.compile(optimizer='adam', loss='binary_crossentropy', 
					metrics=['accuracy'])

	return model

