'''
Client interface for running control flow in document classification
'''
import os
import operator
import threading
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from django.contrib.staticfiles import finders

from DocProc import preprocessing
from .mysql import mySQLConn
from .encoder import encoderFactory
from .evaluate import validateFactory
from .estimator import estimatorFactory
from .transformer import vectorizerFactory, dimensionFactory

# Logger
import logging
logger = logging.getLogger(__name__)

def data_cov(data):
	'''
	converts data to standard format
	'''
	if isinstance(data, dict):
		data = pd.DataFrame.from_dict(data)


	# Renaming columns
	doc_col_names = ['Text','document_text']
	cat_col_names = ['Category']
	doc_ren_name = [x for x in doc_col_names if x in data.columns.values]
	cat_ren_name = [x for x in cat_col_names if x in data.columns.values]

	if doc_ren_name:
		data = data.rename(columns={doc_ren_name[0]:'document'})

	if cat_ren_name:
		data = data.rename(columns={cat_ren_name[0]:'category'})

	# removing null values
	data = data.dropna()

	return data

def data_fetch(svc_data):
	'''
	fetches data from various sources
	'''
	data = dict()

	if svc_data['type'] == 'file':
		# fetches tranining data from file (csv only)
		train_data_path = finders.find(svc_data['filename'])
		data = pd.read_csv(train_data_path)

	elif svc_data['type'] == 'mysql':
		# verification of all db parameters in service request
		db_params = ['host','user','password','database','table','cols']
		if not all([x in svc_data for x in db_params]):
			logger.warning('Parameters missing to get data from MSQL DB')
			raise Exception('Insufficient mysql db params')

		mysql_inst = mySQLConn(svc_data['host'], svc_data['user'], 
								svc_data['password'], svc_data['database'])
		data = mysql_inst.get_data(svc_data['table'], cols=svc_data['cols'])

	else:
		logger.warning('Wrong training data type sent')
		raise Exception('Invalid traninig data type parameter')

	return data

def data_preprocessing(data, token):
	'''
	cleansing and transformation
	'''
	data = data_cov(data)

	# basic language preprocessing
	data['document'] = data['document'].map(lambda doc: 
											preprocessing(doc, type='basic'))

	# encoder instance, saved seperately (thus fit and transform here)
	enc_inst = encoderFactory(encoder='label', token=token)
	data['category'] = enc_inst.fit_transform(data['category'])

	# tranformer instances
	transformers = list()

	# vectorizer instance
	vec_inst = vectorizerFactory(vectorizer='w2v_mean', 
								vectorizer_params={'ngram_range':(1,2)}, 
								token=token, data=data['document'].tolist())

	# dimensionality reducer instance
	# dim_inst = dimensionFactory(reducer='pca') 

	transformers = [('vec',vec_inst)]

	return (data, transformers)

def background_train(svc_data):
	'''
	runs training in a parallel thread, to not make user wait
	'''
	# user input to service
	token = svc_data['token']
	data = data_fetch(svc_data)
	logger.info('Training data obtained')

	# data preprocessing
	data, transformers = data_preprocessing(data, token)
	logger.info('Data preprocessed and transformed')


	# estimator instance, delegates pipeline creation
	est_inst = estimatorFactory(estimator='log', token=token, 
								transformers=transformers)

	# Validation
	# score = validateFactory(est_inst.pipeline_inst, data['document'], 
	# 						data['category'], method='cv', 
	# 						method_params={'cv':5})
	# print ('Accuracy Score: ', score)

	# Model fit and saving
	est_inst.fit(data['document'], data['category'])
	logger.info('Model trained and stored')

def doc_train(svc_data):
	'''
	control flow to run document classification training
	'''
	if 'token' not in svc_data:
		logger.error('Token not sent to save correct model')
		raise Exception('Token absent error')

	if 'type' not in svc_data:
		logger.error('Type not sent for training data')
		raise Exception('Type absent error')

	if 'background' in svc_data and str(svc_data['background']).lower() == 'true':
		logger.info('Background training has started')
		t = threading.Thread(target=background_train, name='background_train',
							args=(svc_data,))
		t.daemon = True
		t.start()

		return 'Training has started in the background. Please check logs to \
		confirm if it finished succesfully.'
	else:
		# synchronous rpc
		background_train(svc_data)
		return 'Model trained succesfully'

def doc_predict(svc_data):
	'''
	make prediction using already stored model
	'''
	if 'token' not in svc_data:
		logger.error('Token not sent to save correct model')
		raise Exception('Token absent error')

	# user input to service
	token = svc_data['token']
	data = svc_data['data']

	# Peform prerpocessing, encoding
	# Standardized data column names
	data = data_cov(data)

	# basic language preprocessing
	data['document'] = data['document'].map(lambda doc: 
											preprocessing(doc, type='basic'))
	logger.info('Data preprocessed')

	# Load encoder and model
	enc_inst = encoderFactory(encoder='label', token=token)
	est_inst = estimatorFactory(estimator='log', token=token)
	logger.info('Models loaded')

	if 'type' in svc_data and svc_data['type'] == 'distribution':
		predictions = dict()
		proba_dis = est_inst.predict_proba(data['document']).to_dict()

		# Decoding labels
		classes = enc_inst.inverse_transform(list(proba_dis.keys()))
		predictions = {x:y[0] for x, y in zip(classes, proba_dis.values())}

		# Rearranging so as to put hightest at top
		predictions = sorted(predictions.items(), key=operator.itemgetter(1), 
								reverse=True)

	else:
		# First make prediction on data, then transform them back
		predictions = est_inst.predict(data['document'])
		predictions = enc_inst.inverse_transform(predictions)

	return predictions

if __name__ == '__main__':
	pass
	# Testing, without django server
	# dir_path = os.path.dirname(os.path.realpath(__file__))
	# train_data_path = dir_path + '/static/documents/BBC News Train.csv'

	# Reading data
	# data = pd.read_csv(train_data_path)

	# training
	# doc_train({'data':data, 'token':'BBC'})

	# prediction
	# predictions = doc_predict({'data':data, 'token':'BBC'})
	# print (predictions)
