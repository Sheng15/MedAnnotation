import couchdb
import json
import datetime
import math

import meshTree


server = couchdb.Server('http://admin:admin@localhost:5984/')

def findToken(token):
	mango = {"selector":{"tree":{"Root": {"children": [{"Anatomy": {"children": [{"Fluids and Secretions": {"children": [{"Body Fluids": {"children": ["Blood"]}}]}}]}}]}}},
			"field" : ['_id'],
			'sort' : [{'_id': 'asc'}]}


def hasToken(token,myList):
	for l in myList:
		if token==l:
			return True
	return False

def category(token):
	tokenConverted = token.title()
	if meshTree.containsToken(tokenConverted):
		nids = meshTree.meshDic[tokenConverted]
		for nid in nids:
			if  ('A' in nid):
				return "Anatomy"
			elif('B' in nid):
				return "Organisms"
			elif('C' in nid):
				return "Diseases"
			elif('D' in nid):
				return "Chemicals_and_Drugs"
			elif('E' in nid):
				return "Analytical_Diagnostic_and_Therapeutic_Techniques_and_Equipment"
			elif('F' in nid):
				return "Psychiatry_and_Psychology"
			elif('G' in nid):
				return "Phenomena_and_Processes"
			elif('H' in nid):
				return "Disciplines_and_Occupations"
			elif('I' in nid):
				return "Anthropology_Education_Sociology_and_Social_Phenomena"
			elif('J' in nid):
				return "Technology_Industry_Agriculture"
			elif('K' in nid):
				return "Humanities"
			elif('L' in nid):
				return "Information_Science"
			elif('M' in nid):
				return "Named_Groups"
			elif('N' in nid):
				return "Health_Care"
			elif('V' in nid):
				return "Publication_Characteristics"
			else:
				return "Geographicals"
	else:
		return "otherTokens"	


def exactSearch(token,db,time = False,limit = 100,TFIDF = False):
	starttime = datetime.datetime.now()
	database = server[db]

	if TFIDF:
		match = {}
		today=datetime.date.today()
		databaseStats = database.get(str(today))
		databaseDocsCount = databaseStats["databaseDocsCount"]
		databaseWordsCount = databaseStats["databaseWordsCount"]

		mango = {'selector':{"tokens."+token:{"$gt":0}},"fields":["_id","tokens."+token,"wordsCount"],"limit":limit}
		for row in database.find(mango):
			##print(row["tokens"][token])
			match[row.id] = [row["tokens"][token],row["wordsCount"]]
		IDF = math.log(databaseDocsCount/(len(match)+1))
		for item in match:
			TF = match[item][0]/match[item][1]
			match[item] = TF * IDF	
		match = sorted(match.items(), key=lambda kv: kv[1])
		match.reverse()
	else:
		match = []
		mango = {'selector':{"tokens."+token:{"$gt":0}},"fields":["_id"],"limit":limit}

		for row in database.find(mango):
			match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match


def semanticSearch(token,db,time = False,limit = 100):
	starttime = datetime.datetime.now()

	database = server[db]

	match = []
	selectors = []

	tokens = meshTree.getDescendants(token)
	for token in tokens:
		selectors.append({"tokens."+token:{"$gt":0}})

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

def tripletsSearch(subject,predicate,obj,db,time = False,limit = 100):
	starttime = datetime.datetime.now()

	database = server[db]

	match = []

	mango = {'selector':{"predications."+subject+predicate+obj:{"$gt":0}},"fields":["_id"],"limit":limit}

	for row in database.find(mango):
		match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match


def predicateSearch(token,predicate,db,time = False,limit = 100):
	starttime = datetime.datetime.now()

	database = server[db]

	match = []

	mango = {'selector':{"$or":[{"predications."+token+predicate:{"$gt":0}},{"predications."+predicate+token:{"$gt":0}}]},"fields":["_id"],"limit":limit}

	for row in database.find(mango):
		match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match

def semanticPredicateSearch(token,predicate,db,time = False,limit = 100):
	starttime = datetime.datetime.now()

	database = server[db]

	match = []
	selectors = []

	tokens = meshTree.getDescendants(token)
	for token in tokens:
		selectors.append({"predications."+token+predicate:{"$gt":0}})
		selectors.append({"predications."+predicate+token:{"$gt":0}})

	##print(selectors)

	mango = {'selector':{"$or":selectors},"fields":["_id"],"limit":limit}

	for row in database.find(mango):
		match.append(row.id)

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)

	return match

def mango(time = False):

	starttime = datetime.datetime.now()

	database = server["demo8search"]

	match = []

	path = "_design/Diseases/_view/new-view"

	mango = {'selector':{"Garbage":{"$gt":1}},"fields":["_id"]}

	for row in database.find(mango):
		print(row["_id"])

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)
		
def mango2(time = False):

	starttime = datetime.datetime.now()

	database = server["demo7"]

	match = []

	path = "_design/Diseases/_view/new-view"

	mango = {'selector':{"$or":[{"Pain":{"$gt":0}},{"Tables":{"$gt":0}}]},"fields":["_id"]}

	print(type(mango))

	for row in database.find(mango):
		print(row["_id"])

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)		

def mango3(tokens,time = False):
	starttime = datetime.datetime.now()

	database = server["demo7"]

	match = []
	selectors = []

	path = "_design/Diseases/_view/new-view"

	for token in tokens:
		selectors.append({token:{"$gt":0}})


	mango = {'selector':{"$or":selectors},"fields":["_id"]}

	for row in database.find(mango):
		print(row["_id"])

	endtime = datetime.datetime.now()
	executionTime = (endtime - starttime).seconds

	if(time == False):
		pass
	else:
		print(executionTime)	












