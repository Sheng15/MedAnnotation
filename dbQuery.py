##author Sheng Tang
##15/10/2018  18：42

'''
use the mothods here to query the database
including :
keyword search
senmatic search
predication search
senmatic & predication search

use mango query that supported by couchdb in version 2.0 or higher
for detail, see "http://docs.couchdb.org/en/2.2.0/api/database/find.html"
'''
import couchdb
import datetime
import math
import termNormalise
import category

import meshTree




def keywordSearch(server,token,db,time = False,limit = 100,TFIDF = False):
	'''
	key word search
	Parameters
	• server – a couchdb server object with admin authority
	• token  - the token to be searched, its a catagory if its in square brackets,"[Disease]"
	• db     – name of a couch database that will search from
	• time   – time = False, do not display the execution time by default
	• limit  – limit = 100, return the first 100 found docs by default
	• TFIDF  – sort = false, not sort the result by TFIDF 
	returns a list of the ids of all docs found
	
	for example:
	docs = keywordSearch(server,"blood","demosearch",time = true,limit = 500, TFIDF = true)
	'''
	starttime = datetime.datetime.now()
	database = server[db]

	if TFIDF:
		match = {}
		###get stats of the database
		stats = database.get("stats")
		databaseDocsCount = stats["DocsCount"]
		databaseWordsCount = stats["WordsCount"]

		### if search for a category
		if token[0] == '[':
			category = token.lower()[1:-1]
			mango = {'selector':{"Category."+category:{"$gt":0}},"fields":["_id","Category."+category,"WordsCount"],"limit":limit}

			for row in database.find(mango):
				match[row.id] = [row["Category"][term],row["WordsCount"]]
			###compute tfidf
			IDF = math.log(databaseDocsCount/(len(match)+1))
			for item in match:
				TF = match[item][0]/match[item][1]
				match[item] = TF * IDF	
			###sort
			match = sorted(match.items(), key=lambda kv: kv[1])
			match.reverse()
		else:
		### search for a particular term
			term = termNormalise.normalise(token.lower())
			mango = {'selector':{"Tokens."+term:{"$gt":0}},"fields":["_id","Tokens."+term,"WordsCount"],"limit":limit}

			for row in database.find(mango):
				#print(row.id)
				match[row.id] = [row["Tokens"][term],row["WordsCount"]]
			###compute tfidf
			IDF = math.log(databaseDocsCount/(len(match)+1))
			for item in match:
				TF = match[item][0]/match[item][1]
				match[item] = TF * IDF	
			###sort
			match = sorted(match.items(), key=lambda kv: kv[1])
			match.reverse()
	else:
		match = []
		if token.lower()[0] == '[':
			category = token.lower()[1:-1]
			mango = {'selector':{"Category."+category:{"$gt":0}},"fields":["_id"],"limit":limit}
		else:
			term = termNormalise.normalise(token.lower())
			mango = {'selector':{"Tokens."+term:{"$gt":0}},"fields":["_id"],"limit":limit}

		for row in database.find(mango):
			match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match


def semanticSearch(server,token,db,time = False,limit = 100):
	'''
	semanticSearch, find docs that contains a token or its descendants
	Parameters
	• server – a couchdb server object with admin authority
	• token  - the token to be searched, its a catagory if its in square brackets,"[Disease]"
	• db     – name of a couch database that will search from
	• time   – time = False, do not display the execution time by default
	• limit  – limit = 100, return the first 100 found docs by default
	returns a list of the ids of all docs found
	'''
	starttime = datetime.datetime.now()

	database = server[db]

	match = []
	selectors = []
	if token[0] == '[':
		cate = token.lower()[1:-1]
		descendants = category.getDescendants(cate)
		for c in descendants:
			selectors.append({"Category."+c:{"$gt":0}})	
		mango = {'selector':{"$or":selectors},"fields":["_id"],"limit":limit}
	else:
		term = termNormalise.normalise(token.lower())
		tokens = meshTree.getDescendants(term)
		#print(tokens)
		for t in tokens:
			selectors.append({"Tokens."+t:{"$gt":0}})

		mango = {'selector':{"$or":selectors},"fields":["_id"],"limit":limit}
		##print(mango)

	for row in database.find(mango):
		match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match

def tripletsSearch(server,subject,predicate,obj,db,time = False,limit = 100):
	'''
	a base case of predicate search. a triplet is a relation that "subject predicate object"
	Parameters
	• server – a couchdb server object with admin authority
	• subject  - the subject token
	• predicate - the predicate token, or relation
	• obj  - the object token
	• db     – name of a couch database that will search from
	• time   – time = False, do not display the execution time by default
	• limit  – limit = 100, return the first 100 found docs by default
	returns a list of the ids of all docs found
	'''
	starttime = datetime.datetime.now()
	database = server[db]
	match = []

	subject_term = termNormalise.normalise(subject.lower())
	obj_term = termNormalise.normalise(obj.lower())

	mango = {'selector':{"Predications."+subject_term+predicate.lower()+obj_term:{"$gt":0}},"fields":["_id"],"limit":limit}

	for row in database.find(mango):
		match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match


def predicateSearch(server,token,predicate,db,time = False,limit = 100):
	'''
	a extend of predicate search. subject or object has not been indicated
	Parameters
	• server – a couchdb server object with admin authority
	• token  - could be a subject or object token
	• predicate - the predicate token, or relation
	• db     – name of a couch database that will search from
	• time   – time = False, do not display the execution time by default
	• limit  – limit = 100, return the first 100 found docs by default
	returns a list of the ids of all docs found
	'''
	starttime = datetime.datetime.now()
	database = server[db]
	match = []

	pre = predicate.lower()
	if token[0] == '[':
		cate = token.lower()[1:-1]
		mango = {'selector':{"$or":[{"Predications."+cate+pre:{"$gt":0}},{"Predications."+pre+cate:{"$gt":0}}]},"fields":["_id"],"limit":limit}
		print(mango)

	else:
		term = termNormalise.normalise(token.lower())
		mango = {'selector':{"$or":[{"Predications."+term+pre:{"$gt":0}},{"Predications."+pre+term:{"$gt":0}}]},"fields":["_id"],"limit":limit}
		print(mango)

	for row in database.find(mango):
		match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match

def semanticPredicateSearch(server,subject,predicate,obj,db,time = False,limit = 100):
	'''
	a combination of semantic search and predicate search expand all possible candidates
	Parameters
	• server – a couchdb server object with admin authority
	• subject  - the subject token，can also be a category
	• predicate - the predicate token, or relation
	• obj  - the object token，can also be a category
	• db     – name of a couch database that will search from
	• time   – time = False, do not display the execution time by default
	• limit  – limit = 100, return the first 100 found docs by default
	returns a list of the ids of all docs found
	'''
	starttime = datetime.datetime.now()
	database = server[db]
	match = []
	selectors = []

	if (subject[0] != '[') and (obj[0] != '['):
		
		subjects = meshTree.getDescendants(subject.lower())
		#print(subjects)
		
		objs = meshTree.getDescendants(obj.lower())
		print(objs)
		for s in subjects:
			print(s)
			for o in objs:
				print(o)
				selectors.append({"Predications."+s+predicate.lower()+o:{"$gt":0}})
				print(s+predicate.lower()+o)

	elif subject[0] == '[' and obj[0] != '[':
		cate = subject.lower()[1:-1]
		descendants = category.getDescendants(cate)
		objs = meshTree.getDescendants(obj.lower())

		for d in descendants:
			for o in objs:
				selectors.append({"Predications."+d+predicate.lower()+o:{"$gt":0}})
				print(d+predicate.lower()+o)
	else:
		subjects = meshTree.getDescendants(subject.lower())
		print(subjects)
		cate = obj.lower()[1:-1]
		descendants = category.getDescendants(cate)

		for s in subjects:
			for d in descendants:
				selectors.append({"Predications."+s+predicate.lower()+d:{"$gt":0}})

	mango = {'selector':{"$or":selectors},"fields":["_id"],"limit":limit}
	print(mango)
	for row in database.find(mango):
		match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match

