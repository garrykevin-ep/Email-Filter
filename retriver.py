from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors
import dateutil.parser as parser
import base64
import sqlite3


SCOPES = 'https://mail.google.com/'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))


def ListMessages(service, user_id):
  try:
    response = service.users().messages().list(userId=user_id).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print (error)

def GetEmailContent(service,user_id,emailId):
	response = service.users().messages().get(userId=user_id,id=emailId).execute()
	return response

def GetHeaderValue(name,headers):
	for header in headers:
		if header['name'] == name:
			return header['value']

def GetContentFromEmail(service, user_id, msg_id):
  """
  Returns:
    A dict , consisting of data from recivedfrom,date,body,subject.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()   
    payload = message['payload']
    headers = payload['headers']
    msg_date = GetHeaderValue('Date',headers)
    date_parse = parser.parse(msg_date)
    msg_time = date_parse.time()
    msg_date = date_parse.date()
    content = {
    	'Subject' : GetHeaderValue('Subject',headers),
    	'Date'  : str(msg_date),
    	'Time'  : str(msg_time),
    	'From'  : GetHeaderValue('From',headers),
    	'Body' 	: message['snippet'],
    	'Id'	:	msg_id
    }
    return content
  except errors.HttpError, error:
    print ('An error occurred: ')

def insertDb(content):
	try:
		conn = sqlite3.connect('db.db')
		query = 'INSERT INTO Email (id,subject,date,time,body) VALUES ("{}","{}","{}","{}","{}")'.format(content['Id'],content['Subject'],content['Date'],content['Time'],content['Body'])
		# print (query)
		conn.execute(query)
		conn.commit()
		conn.close()
	except sqlite3.Error as er:
		pass
		# print (er)

def main():
  emails = ListMessages(service,'me') 
  for email in emails:
    email_content = GetContentFromEmail(service,'me',email['id'])
    insertDb(email_content)


if __name__ == '__main__':
  # main()
	
# service.users().messages().get(userId='me', id=emails[0]['id']).execute()
# payld = message['payload']
	print ("import is here")
# print "import is here"