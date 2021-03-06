##author Sheng Tang
##08/09/2018  16:40



##mainly use couchdb-python library，source code at https://github.com/djc/couchdb-python
##Document can be find at https://couchdb-python.readthedocs.io/en/latest/



###########################################################################################################
#############   Methods that can be used to perform basic database process                    ############# 
#############	inclouding：connect server, authentication，create user，set database member， #############
###########################################################################################################
#python3

import couchdb
import sys
import os
import fileProcesser 
import mmh3




###############################################################################################
###############################    connect to couch db   ######################################
###############################################################################################

'''
recommendation of general usage there：
server = connect(ip_address) //get a basic couch server
try :
	authentication = loginUser(server，username， password) 
	authServer = authConnection(ip_address,username,password)
	logoutuser(authentication)
except Exception as e:
	print("failed to establish an authentication connection!")

## this will make sure only establish valid connection
## should have some better solution there！！

'''

def connect(ip_address):
	'''
	This gets you a Server object, representing a CouchDB server. 
	pass the ip_address, the port should also be provided.

	Parameters
	• ip_address  – the ip_address of couchdb server, the port should also be provided.
	Returns a couchdb server object

	By default, let assumes CouchDB is running on localhost:5984,
	pass ip_address = "http://localhost:5984",
	If CouchDB server is running elsewhere, set it up like this:
	ip_address = "http://otherIP_address:5984"

	'''
	server = couchdb.Server(ip_address)
	return server
	## it is only a server object without any checking whether the 
	## server is running or not

def authConnection(ip_address,username,password):
	'''
	pass authentication credentials and/or use SSL to create a 
	server object with all the authority the user has 
	but the validation of username and password is absent
	Parameters
	• ip_address – the ip_address of couchdb server, the port should also be provided.
	• username 	 – name of regular user, normally user id
	• password   – password of regular user
	Returns a couchdb server object
	'''
	credentials = "http://"+username+":"+password+"@"+ip_address
	server = couchdb.Server(credentials)
	return server


def loginUser(server,username,password):
	'''
	Login regular user in couchDB
	Parameters
	• server   –	a couchDB server to login 
	• username – 	name of regular user, normally user id
	• password – 	password of regular user
	Returns authentication token
	'''
	try:
		authentication = server.login(username,password)
		print("login as "+username+" successfully!")
		return authentication
		## it only used for authentication check
		## it will not create a server object with any authority
	except Exception as e:
		print("login failed!")


def logoutUser(server,authentication):
	'''
	Logout regular user in couch 
	• server 		 –	a couchDB server to login 
	• authentication – 	authentication token
	
	returns true if logout successfully.
    '''
	try:
		server.logout(authentication)
		print("logout successfully")
	except Exception as e:
		print("logout failed")

###########################################################################
##########################  database permission   #########################
###########################################################################


def setPermissions(server,db,admins,members):
	'''
	set the admins and members of a database
	admins have admins access to this database.
	members have members access to this database.
	admin access is allowed to do anything to the database.
	member access is allowed to write (and edit) documents to the DB except for design documents.
	the role of a user is left blank for further development.
	for more detail,see http://docs.couchdb.org/en/stable/api/database/security.html
	Parameters
	• server  – a couchdb server object with admin authority
	• db 	  – the name of database that being set permission
	• admins  – a list of user names of users to be set as admins of the database
	• members – a list of user names of users to be set as members of the database

	raise exception is failed to set 
	'''

	## a database is public(everyone is admin) if no admin and member is defined!
	## set permission immediately after the database is created.
	## However, this method will just set the permissions according to the given list,
	## without any check that whether the given user is exist 
	## this method will over write any former set！！！！

	try:
		database = server[db]
		database.resource.put("_security",{u'admins': {u'names':admins,u'roles': []},u'members': {u'names': members, u'roles': []}})
		print("set permission successfully")
	except Exception as e:
		print(e)
	
def permissionInfo(server,db):
	'''
	fetch the permissionInfo of a database
	Parameters
	• server – a couchdb server object with  authority
	Returns a dict of current admins and members or raise exception
	for example: 
	{'admins': {'names': ['admin1', 'admin2', 'admin3'], 'roles': []}, 'members': {'names': ['member1'], 'roles': []}}
	'''
	try:
		database = server[db]
		security_doc=database.resource.get_json("_security")[2]
		return security_doc
	except Exception as e:
		print(e)	

def updatePermission(server,db,newPermission):
	'''
	uapate permission with provided without overwrite old permission 
	'''
	print("TO BE IMPLEMENTED FURTHER")


###############################################################################################
#######################               user management                       ###################
###############################################################################################	

def addUser(ip_address,adminUserName,adminPassword,username,password):
	'''
	create a user to the database, three things have been done.
	1. create and add a new user to couch if not collide；
	2. create two database for this user
	3. set permission of the new database
	Parameters
	• server   – a couchdb server object with admin authority
	• username – name of regular user, normally user id
	• password – password of regular user
	raise exception if there is 
	'''
	try:
		##step 1: create and add user
		server = authConnection(ip_address,adminUserName,adminPassword)
		server.add_user(username,password)
		##step 2: create database
		## database named with "user" will used to store original files
		## database named with “userSearch” will used as an insex of former db
		database = username
		databaseSearch = username + "search"
		server.create(database)
		server.create(databaseSearch)
		### init stats
		_doc = {
			"WordsCount":0,
			"DocsCount":0
			}
		databaseSearch[stats] = _doc
		##step 3: set permission
		admins = [adminUserName,username]
		members = [adminUserName,username]
		setPermissions(server,database,admins,members)
		setPermissions(server,databaseSearch,admins,members)

	except Exception as e:
		print(e)


def removeUser(server,username,purge = False):
	'''
	remove a user 
	Parameters
	• server   – a couchdb server object with admin authority
	• username – name of regular user, normally user id
	• purge    – delete the users' database when remove the user(purge = False, not purge by default)
	raise exception if there is 
	'''
	if not purge:
		try:
			server.remove_user(username)
		except Exception as e:
			print("failed to remove user")
	else:
		## purge a user
		try:
			server.remove_user(username)
			server.delete(username)
			server.delete(username+"search")
		except Exception as e:
			print("failed to remove user")


########################################################################################################
####################  simple method to get original clinical trials and annotation   ###################
####################  		especially when the ID in database is given  			 ###################
########################################################################################################

def get(server,db,id):
	'''
	get the clinical trial and annotation file from a particular document in the database 
	Parameters
	• server – a couchdb server object with admin authority
	• db     – name of a couch database that save the original clinical files and annotations
	• id   	 – identifier of a document in couch database，
	raise exception if there is
	returns clinical trial and its annotation file
	'''
	try:
		database = server[db]
		_doc = database.get(id)
		clinical_trial = _doc[Clinical_Trial]
		annotation = _doc[Annotation]
		return clinical_trial,annotation
	except Exception as e:
		print(e)


def get_annotation(server,db,file,user):
	'''
	find the annotation made by a particular user to a particular clinical trial
	Parameters
	• server – a couchdb server object with admin authority
	• db     – name of a couch database that save the original clinical files and annotations
	• file   - path of a clinical trial
	• user 	 - identifier of the user， usually the user name
	returns the annotation file 
	'''
	text = fileProcesser.readFile(file)
	doc_id = fileProcesser.computeID(text,user)

	annotation = get(server,db,doc_id)[1]
	return annotation

def get_annotation_all(server,db,file):
	'''
	find all the annotations made  to a particular clinical trial
	Parameters
	• server – a couchdb server object with admin authority
	• db     – name of a couch database that save the original clinical files and annotations
	• file   - path of a clinical trial
	returns the id as an array of all documents found in databse
	'''

	result = []
	database = server[db]

	text = fileProcesser.readFile(file)
	text_id = str(mmh3.hash(text,signed=False))
	start_key= text_id
	end_key = text_id +"ZZZZZZZZZZ"

	for item in database.view('_all_docs', startkey=start_key, endkey=end_key):
		result.append(item.id)

	return result