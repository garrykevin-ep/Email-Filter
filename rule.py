import json
import sqlite3

conn = sqlite3.connect('db.db')

def GetConfig():
	with open('config.json') as json_file:
		data = json.load(json_file)
		return data



def ListEmailsContain(entity,text):
	"""
	arg1 - where
	arg2 - what it contains
	return tuple containing 
	"""
	try:
		conn = sqlite3.connect('db.db')
		query = 'SELECT * from Email where {} like "%{}%" '.format(entity,text)
		cursor = conn.execute(query)
		# for row in cursor:
		# 	print row
		return cursor
	except sqlite3.Error as er:
		print (er)
	pass

def ListAllEmail():
	try:
		conn = sqlite3.connect('db.db')
		query = 'SELECT * from Email'
		cursor = conn.execute(query)
		conn.close()
		return cursor
	except sqlite3.Error as er:
		print (er)
		pass

def ListNotContains(entity,text):
	# emails_contains = ListEmailsContain(entity,text)
	# emails = ListAllEmail()
	try:
		query = 'SELECT * from Email where {} not like "%{}%" '.format(entity,text)
		# print (query)
		cursor = conn.execute(query)
		# for row in cursor:
		# 	print row
		return cursor
	except Exception as e:
		raise e
	pass

def Intersection(items1,items2):
	items1 = set(items1)
	items2 = set(items2)
	print( items1.intersection(items2) )


# result = set()#contains all emails

# print (result)

# configs = GetConfig()

# toprule = list(configs.keys())[0]
# print (toprule)
# rules_list = configs[toprule] #list of contains, not contains
# for rule in rules_list:	#single rule
# 	# print (rule) #dict
# 	predicate = rule.keys()[0]
# 	print (predicate)
# 	for constraint in rule[predicate]:
# 		print (constraint)
# 		predicate = predicate.keys()[0]
# 		if predicate == 'contains':
# 			temp_result = ListEmailsContain(key,predicate[key])
# 			#set intersection
# 		elif predicate == 'notcontains':
# 			temp_result = ListNotContains(key,predicate[key])
# 			#set intersection
# 		elif predicate == 'older':
# 			pass
# 			#set intersection


#set add if contains
#set difrrence if not contains
#set diffrence if date  query



items1  = ListEmailsContain('subject','confidential')
for email  in  items1:
	print (email)

items2  = ListNotContains('subject','confidential')
for email in items2:
	print (email)

Intersection(items1,items2)


conn.close()
