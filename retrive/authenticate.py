from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


SCOPES = 'https://mail.google.com/'

def build_service():
	"""Build a Gmail service object.

	  Returns:
	    Gmail service object.
 	 """

	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
	    creds = tools.run_flow(flow, store)
	service = build('gmail', 'v1', http=creds.authorize(Http(disable_ssl_certificate_validation=True)))
	return service