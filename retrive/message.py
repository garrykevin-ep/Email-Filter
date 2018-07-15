from authenticate import build_service
import dateutil.parser as parser
from dateutil.utils import today
from apiclient import errors
from db import Db
import datetime

class Store(object):

 	def __init__(self,user_id='me'):
 		self.user_id = user_id
 		self.service = build_service()
 		print ("Retriving Messages from gmail...")
 		self.list_messages()
 		print ("Messages Retrived")
 		print ("Storing Messages....")
 		self.store_email()
 		self.store_labels()
 		print ("Stored Messages")
  	
  	def list_messages(self):
  		"""
  		gmail api returns thread ids
  		"""
		try:
			response = self.service.users().messages().list(userId=self.user_id).execute()
			self.messages = []
			if 'messages' in response:
				self.messages.extend(response['messages'])

			while 'nextPageToken' in response:
				page_token = response['nextPageToken']
				response = self.service.users().messages().list(userId=user_id, q=query,
				pageToken=page_token).execute()
				self.messages.extend(response['messages'])
		except errors.HttpError, error:
			print (error)

	def get_header_value(self,name,headers):
		"""
		helper method
		date,subject are available in headers
		"""
		for header in headers:
			if header['name'] == name:
				return header['value']

	def get_content_from_email(self,user_id, msg_id):
		"""
		Returns:
		A dict , consisting of data from recivedfrom,date,body,subject.
		"""
		try:
			message = self.service.users().messages().get(userId=user_id, id=msg_id).execute()
			payload = message['payload']
			headers = payload['headers']
			msg_date = self.get_header_value('Date',headers)
			date_parse = parser.parse(msg_date)
			msg_time = date_parse.time()
			msg_date = date_parse.date()
			content = {
				'Subject' : self.get_header_value('Subject',headers),
				'Date'  : str(msg_date),
				'Time'  : str(msg_time),
				'From'  : self.get_header_value('From',headers),
				'Body' 	: message['snippet'],
				'Id'	:	msg_id,
				'Labels' : message['labelIds']
			}
			return content
		except errors.HttpError, error:
			print ('An error occurred: ')

	def store_email(self):
		'''
		iterates through all messages extacts information using ids
		then stores in Db
		'''
		self.messages_content = []
		self.labels_content = []
		for message_content in self.messages:
			email_content = self.get_content_from_email('me',message_content['id'])
			content = {
			'values' : [ email_content['Id'],email_content['Subject'],email_content['Date'],email_content['Time'],email_content['Body']],
			'labels' : [ email_content['Id'],email_content['Labels'] ]
			}
			self.messages_content.append(content['values'])
			self.labels_content.append(content['labels'])
		db = Db()
		db.insert_bulk_email(self.messages_content)
		db.insert_bulk_email_labels(self.labels_content)

 	def store_labels(self):
 		'''
		iterates through all messages extacts labels
		then stores in Db
		'''
 		self.labels = []
 		try:
 			response = self.service.users().labels().list(userId=self.user_id).execute()
 			for label in response['labels']: 
 				self.labels.append( [ label['id'],label['name'] ] )
 			db = Db()
 			db.insert_labels(self.labels)
 		except errors.HttpError,error:
 			print (error)	

class Filter():

	columns = {
	'id' : 0,
	'subject' : 1,
	'date' : 2,
	'time' : 3,
	'body' : 4,
	}

	def __init__(self,emails,filter_type):
		self.emails = set(emails)#input
		self.result = set()#output
		self.filter_type = filter_type

	def has_word(self,text,word_match):
		words = text.split()
		for word in words:
			if word == word_match:
				return True
		return False

	def make_result(self):
		if self.filter_type == 'AND':
			self.emails = self.emails.intersection(self.result)
			self.result.clear()

	def emails_contain(self,column,word):
		for email in self.emails:
			if self.has_word( email[ self.columns[column] ],word):
				self.result.add(email)

	def emails_not_contain(self,column,word):
		self.emails_contain(column,word)
		self.result = self.emails - self.result
		
	def older_than(self,column,days):
		for email in self.emails:
			email_date = parser.parse( email[ self.columns['date'] ])
			now = datetime.datetime.now()
			relative_days = (now - email_date).days
			if relative_days < days:
				self.result.add(email)

	def not_older_than(self,column, days):
		self.older_than(column,days)
		self.result = self.emails - self.result
