'''
Interface to push training data onto database, parsed by local machine
'''
from documents import mySQLConn

# Logger
import logging
logger = logging.getLogger(__name__)

def data_echo(svc_data):
	'''
	method to connect with database and push data
	'''
	# payload check
	db_params = ['host','user','password','database', 'document_text', 
				'document_name', 'category']
	if not all([x in svc_data for x in db_params]):
		logger.warning('Parameters missing to get data from MSQL DB')
		raise Exception('Insufficient mysql db params')

	document_name = svc_data['document_name']
	document_text = svc_data['document_text']
	category = svc_data['category']

	# prevention from entering empty or invalid data
	if (not document_name or not document_text or not category or 
		not isinstance(document_name, str) or 
		not isinstance(document_text, str) or 
		not isinstance(category, str)):
		logger.warning('Invalid data being inserted')
		raise Exception('Invalid data sent')

	# The table details have been hardcoded within service, for security
	table_name = 'training_data'

	# creating DB connection
	mysql_inst = mySQLConn(svc_data['host'], svc_data['user'], 
							svc_data['password'], svc_data['database'])

	# Pushing the data
	mysql_inst.put_data(table_name, ['document_name','document_text',
						'category'], [document_name, document_text, category])
