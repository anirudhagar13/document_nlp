'''
Class containing modules to evaluate classification models
'''
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

# Logger
import logging
logger = logging.getLogger(__name__)

def validateFactory(pip_inst, X, y, method='cv', method_params=dict()):
	'''
	Factory to delegate method calling
	'''
	# Delegation
	if method == 'cv':
		# expected parama {'cv':5}
		scores = cross_val_score(pip_inst, X, y, **method_params)
		return sum(scores) / len(scores)

	elif method == 'tt':
		# expected parama {'test_size':0.25}
		X_train, X_test, y_train, y_test = train_test_split(X, y, 
															**method_params)
		pip_inst.fit(X_train, y_train)
		return accuracy_score(y_test, pip_inst.predict(X_test))
	
	else:
		logger.warning('Invalid Validation choice !!')
		sys.exit(0)

	return 