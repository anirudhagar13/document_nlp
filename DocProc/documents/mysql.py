# Instance to connect to mysqldb, store and fetch data
import pandas as pd
import mysql.connector

class mySQLConn:
	def __init__(self, host, user, password, database):
		self.mydb = mysql.connector.connect(host=host, user=user, 
											passwd=password, database=database)
		self.mycursor = self.mydb.cursor()

	def get_data(self, table, cols=[]):
		'''
		return all data from table mentioned
		'''
		query = "SELECT * FROM " + table

		if cols:
			query = query.replace('*', ','.join(cols))

		# query execution and record fetch
		self.mycursor.execute(query)
		records = self.mycursor.fetchall()

		# package in a dataframe and send back
		data = list()
		for record in records:
			temp = dict()
			for index, col_name in enumerate(cols):
				temp[col_name] = record[index]

			data.append(temp)

		return pd.DataFrame(data)

	def put_data(self, table, cols=list(), data=list()):
		'''
		inserts data one by one, assuming data is a list of lists
		'''
		query = "INSERT INTO {0} ({1}) VALUES (%s, %s, %s)".format(table, 
															','.join(cols))

		# Can insert one row at a time, bulk insert not supported as of now
		self.mycursor.execute(query, data)

		## to make final output we have to run the 'commit()'
		self.mydb.commit()

	def __str__(self):
		return 'mySQLConn instance to connect and store data in MySQL DB'
