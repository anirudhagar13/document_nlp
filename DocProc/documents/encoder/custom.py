from sklearn.preprocessing import LabelEncoder
from sklearn.exceptions import NotFittedError

# Implementing abstract class
from .abstract import Encoder

# Logger
import logging
logger = logging.getLogger(__name__)

class ModifiedLabelEncoder(Encoder):
	def __init__(self, model_path='', model_params=dict()):
		'''
		To define default parameters
		'''
		if not model_path:
			logger.error('Model path sent to ModifiedLabelEncoder is emtpy')
			raise Exception('Model path not sent')
			
		self._model_path = model_path
		self.model = LabelEncoder()

	def fit(self, y):
		logger.info("ModifiedLabelEncoder 'fit' module")

		# Fitting
		self.model.fit(y)	

		# Save model using default implementation
		super().save_model(self.model, self._model_path, 'labelencoder')

		return self.model

	def transform(self, y):
		'''
		Loads old model
		'''
		logger.info("ModifiedLabelEncoder 'transform' module")
		transformed = list()
		
		try:
			# Making transformation
			transformed = self.model.transform(y)

		except NotFittedError as e:
			# Load previously saved model using default implementation
			self.model = super().load_model(self._model_path, 'labelencoder')

			# Making predictions
			transformed = self.model.transform(y)		

		return transformed

	def fit_transform(self, y):
		'''
		First fits then transforms data
		'''
		self.fit(y)
		return self.transform(y)

	def inverse_transform(self, y):
		'''
		Loads old model
		'''
		logger.info("ModifiedLabelEncoder 'inverse_transform' module")
		transformed = list()
		
		try:
			# Making transformation
			transformed = self.model.inverse_transform(y)

		except NotFittedError as e:
			# Load previously saved model using default implementation
			self.model = super().load_model(self._model_path, 'labelencoder')

			# Making predictions
			transformed = self.model.inverse_transform(y)		

		return transformed

	def __str__(self):
		'''
		Makes class printable
		'''
		return 'ModifiedLabelEncoder'

