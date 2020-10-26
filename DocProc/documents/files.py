# Contains re-usable file related operations
import os
import csv
import json
import pandas as pd
import dill as pickle

# Logger
import logging
logger = logging.getLogger(__name__)

# Getting absolute path
dirpath = os.path.dirname(__file__)
if dirpath:
	# To compensate relative paths
	dirpath += '/'

def getAbspath():
	'''
	returns absolute directory path till this module
	'''
	return dirpath

def read_to_string(inpfile_path):
	'''
	Function that returns content of a file in a string
	'''
	data = ''
	inpfile_path = dirpath + inpfile_path
	try:
		with open(inpfile_path, 'r') as inp_file:
			data = inp_file.read().replace('\n', ' ')
	except Exception as e:
		logger.error("'read_to_string' - Issue with file : ",e)

	return data

def read_from_json(inpfile_path):
	'''
	Reads json file and return data
	'''
	data = dict()
	inpfile_path = dirpath + inpfile_path
	try:
		with open(inpfile_path,'r') as inpfile:
			data = json.load(inpfile)
	except Exception as e:
		logger.error("'read_from_json' - Issue with file : ",e)

	return data

def read_from_pkl(inpfile_path):
	'''
	Reads pickle file and return data
	'''
	data = ''
	inpfile_path = dirpath + inpfile_path
	try:
		with open(inpfile_path,'rb') as inpfile:
			data = pickle.load(inpfile)
	except Exception as e:
		logger.error("'read_from_pkl' - Issue with file : ",e)
		raise Exception(e)

	return data

def read_from_excel(inpfile_path, sheet_name=None):
	'''
	Reads excel file and return dataframe or OrderedDict
	'''
	data = pd.DataFrame
	inpfile_path = dirpath + inpfile_path
	try:
		data = pd.read_excel(inpfile_path, sheet_name=sheet_name)
	except Exception as e:
		logger.error("'read_from_excel' - Issue with file : ",e)

	return data

def read_from_csv(inpfile_path, delimiter=','):
	'''
    Reads data from csv file and returns a dataframe
    '''
	data_table = []
	try:
		with open(inpfile_path, 'r') as csvfile:
			filereader = csv.reader(csvfile, delimiter=delimiter)
			for row in filereader:
				data_table.append(row)
	except Exception as e:
 		logger.error("'read_from_csv' - Issue with file : ",e)

    
	# Converting list to dataframe
	headers = data_table.pop(0)
	df = pd.DataFrame(data_table, columns=headers)
    
	return df

def read_big_csv(inpfile_path, delimiter=',', chunk_size=1000):
	'''
	Generator fun to read big csv file in chunks of 1000 rows or less
	'''
	counter = 0
	headers = list()
	data_table = list()

	try:
		with open(inpfile_path, 'r') as csvfile:
			filereader = csv.reader(csvfile, delimiter=delimiter)
			for row in filereader:
				if counter == 0:
					# Storing heading
					headers = row

				else:
					# Appending to datalist and increasing counter
					data_table.append(row)

				counter += 1
				if counter % chunk_size == 0:
					df = pd.DataFrame(data_table, columns=headers)

					# Empty list and send back dataframe
					data_table = list()
					yield df

	except Exception as e:
 		logger.error("'read_from_csv' - Issue with file : ",e)

 	# Sending remaining of file left after chunking
	df = pd.DataFrame(data_table, columns=headers)
	yield df

def write_to_csv(df, outfile_path, mode='w', header=True, sep=','):
	'''
	Writes dataframe to csv file
	'''
	try:
		df.to_csv(outfile_path, index=False, mode=mode, header=header, sep=sep)
	except Exception as e:
 		logger.error("'write_to_csv' - Issue with file : ",e)

def write_to_excel(df, outfile_path, sheet_name='Sheet 1'):
	'''
	Writes dataframe to excel file
	'''
	try:
		writer = pd.ExcelWriter(outfile_path)
		df.to_excel(writer, sheet_name)
		writer.save()
	except Exception as e:
 		logger.error("'write_to_excel' - Issue with file : ",e)

def write_to_json(data, outfile_path, mode='w'):
 	'''
 	Dumps data into json file, data should be a formattable json
 	'''
 	outfile_path = dirpath + outfile_path

 	try:
 		with open(outfile_path, mode) as outfile:
	 		json.dump(data, outfile, indent=4)
 	except Exception as e:
 		logger.error("'write_to_json' - Issue with file : ",e)

def write_to_pkl(data, outfile_path, mode='wb'):
 	'''
 	Dumps data into pickle file, data should be a formattable pickle
 	'''
 	outfile_path = dirpath + outfile_path

 	try:
 		with open(outfile_path, mode) as outfile:
	 		pickle.dump(data, outfile)
 	except Exception as e:
 		logger.error("'write_to_pkl' - Issue with file : ",e)		