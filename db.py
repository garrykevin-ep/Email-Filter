import sqlite3
from query import *

class Db():
	
	def __init__(self, *args, **kwargs):
	    self.conn = sqlite3.connect('db.db')
	    self.conn.executescript(TABLE_SCHEMA)
	
	def insert_labels(self,values):
		try:
			self.conn.executemany(LABEL_INSERT,values)
			self.conn.commit()
		except sqlite3.Error as er:
			print (er)
			pass
	
	def insert_bulk_email_labels(self,labels):
		try:
			for email_id,label in labels:
				query = EMAIL_LABEL_INSERT.format(email_id)
				label_list = [[slabel]for slabel in label]
				self.conn.executemany(query,label_list)
				self.conn.commit()
		except sqlite3.Error as er:
			print (er)
			pass

	def insert_bulk_email(self,emails):
		try:
			self.conn.executemany(EMAIL_BULK_INSERT,emails)
			self.conn.commit()
		except sqlite3.Error as er:
			print (er)
	
	def insert_email(self,content):
		try:
			query = EMAIL_INSERT.format(content['Id'],content['Subject'],content['Date'],content['Time'],content['Body'])
			self.conn.execute(query)
			self.conn.commit()
		except sqlite3.Error as er:
			print (er)
			pass


	def print_results(self):
		for result in self.results:
			print (result)
	
	def get_emails(self):
		query = 'select * from email'
		rows = self.conn.execute(query)
		return [row for row in rows]


	def list_row(self,query):
		self.results = self.conn.execute(query)
		self.conn.commit()

	def __del__(self):
		self.conn.close()