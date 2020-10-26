'''
Class containing modules to evaluate classification models
'''
from .custom import ModifiedLabelEncoder

# Logger
import logging
logger = logging.getLogger(__name__)

def encoderFactory(encoder='label', token='XXXX', encoder_params=dict()):
	'''
	Factory to delegate method calling
	'''
	# Initialization
	model_path = ('encoder/models/' + token + '_enc.pkl')

	# Delegation
	if encoder == 'label':
		return ModifiedLabelEncoder(model_path=model_path)
			
	else:
		logger.warning('Invalid Encoder choice !!')
		sys.exit(0)

	return 