# Factory for estimator instance

import sys
from .sklearn_est import SKEstimator

# Logger
import logging
logger = logging.getLogger(__name__)

sklearn_types = ['naive','log','svm','linearsvc','svmsvc','random','bag',
					'gboost','adaboost','deepnet']

def estimatorFactory(estimator='naive', token='XXXX', model_params=dict(), 
						transformers=None):
	'''
	Factory to delegate instance creation
	'''
	
	# Initialization
	estimator_inst = object()
	model_path = ('estimator/models/' + token + '.pkl')

	# Delegation
	if estimator in sklearn_types:
		# Instantiating common interface for all sklearn models
		estimator_inst = SKEstimator(estimator=estimator,
										model_params=model_params,
										transformers=transformers,
										model_path=model_path)

	else:
		logger.warning('Invalid Estimator Choice !!')
		sys.exit(0)

	return estimator_inst
