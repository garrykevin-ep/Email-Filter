# from __future__ import print_function
# from apiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools
# from apiclient import errors
# import dateutil.parser as parser
# import base64
# import sqlite3

# print ('Hey retrive')
# SCOPES = 'https://mail.google.com/'
# store = file.Storage('credentials.json')
# creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
#     creds = tools.run_flow(flow, store)
# service = build('gmail', 'v1', http=creds.authorize(Http()))
