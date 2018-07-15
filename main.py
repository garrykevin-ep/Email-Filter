from retrive.message import Store,Filter
from retrive.authenticate import build_service
from db import Db
import json


class ReadConfig():
	'''
		Filters iterate thorugh the rules
		and stores the result
	'''

	def __init__(self):
		self.result = set()
	 	with open('config.json') as json_file:
	 		self.data = json.load(json_file)
	
	def iterate(self,data,filter_type):
		emails = Db().get_emails()
		filters = Filter(emails,filter_type)
		keys = data.keys()
		for predicate in keys:
	 		for column,match in data[predicate]:
	 			if predicate == 'contains':
	 				filters.emails_contain(column,match)
	 			elif predicate == 'notcontains':
	 				filters.emails_not_contain(column,match)
	 			elif predicate == 'older':
	 				filters.older_than( column , int(match) )
	 			elif predicate == 'notolder':
	 				filters.not_older_than( column , int(match) )
	 			filters.make_result()
	 	if filter_type == 'AND':
	 		self.result = self.result.union(filters.emails)
	 	else:
	 		self.result = self.result.union(filters.result)


	def iterate_and(self):
		self.iterate(self.data['AND'],'AND')

	def iterate_or(self):
		self.iterate(self.data['OR'],'OR')

	def perfrom_action(self):
		body = {
		'ids' : [ id[0] for id in self.result ]
		}

		if len (self.data['DO']['add']):
			body['addLabelIds']	 = self.data['DO']['add']
		
		if len ( self.data['DO']['remove'] ):
			body['removeLabelIds']	= self.data['DO']['remove'] 
		
		service = build_service()
		service.users().messages().batchModify(userId='me',body=body).execute()
		
#Task 1
Store() #gets email and strores in DB

# Task2
config = ReadConfig() #read 
config.iterate_and() #perform "and" rules
config.iterate_or() #perform "or" rules
config.perfrom_action() #do specified action
