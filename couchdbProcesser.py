##author Sheng Tang
##08/09/2018  16:40

##library used is couchdb-python from https://github.com/djc/couchdb-python
##Document can be find at https://couchdb-python.readthedocs.io/en/latest/



######################################################################################################
#############	general methods that can be invoked to perform basic database process    ############# 
#############	inclouding：query view，query a grouped view，obtain data，save file     #############
#############                or data into couchdb. And a method to create view           #############
###################################################################################################### 
#python3

import couchdb
import json
import sys
import os
import mmh3
import fileProcesser 
import datetime

from treelib import Node, Tree


##connect to database, "admin" as the user name and password to make our life easier
server = couchdb.Server('http://admin:admin@localhost:5984/')
#server = couchdb.Server('http://localhost:5984/')




###########  support functions ######################

def readFile(file):
	f = open(file,'r')
	result = ''
	for line in f.readlines():
		result = result+line
	f.close()
	return result

def computeID(text,user):
	## id of document
	text_id = str(mmh3.hash(text,signed=False))
	user_id = str(mmh3.hash(user,signed=False))
	id = text_id+user_id
	return id


#########simple get,query,obtain,save methods #############

def get_text(db,text_file,user):

	database = server[db]

	text = readFile(text_file)
	id = computeID(text,user)

	doc = database.get(id)
	return doc


def get_text_all(db,text_file):
	database = server[db]

	text = readFile(text_file)
	text_id = str(mmh3.hash(text,signed=False))
	start_key= text_id
	end_key = text_id +"ZZZZZZZZZZ"

	for item in database.view('_all_docs', startkey=start_key, endkey=end_key):
		print(item.id)




def query_view(db,viewName):

	##connect to databse
	databse = server[db]

	## query view from couchdb
	result = db.query(viewName+"/id_str")

	return list(result)

def query_grouped_view(db,viewName):
	##query view that is grouped

	##connect to databse
	db = server.database(db)

	## query view from couchdb
	result = db.query(viewName+"/id_str",group='true')

	return list(result)


def get_data(db,docID):

	##connect to databse
	database = server[db]

	# get data
	result=db.get(docID)

	return result


def save_file(db,file):
	#save json file into couchdb

	##connect to databse
	database = server[db]

	#load json file
	fload = open(file,'r')
	doc = json.load(fload)

	db.save(doc)

def save_text(db,text):

	_doc ={
		"_id":id,
		"text":text,
	} 

	##connect to databse
	database = server[db]

	database.save(_doc)

def save_annotated_text(db,text_file,user,annotation_file):
	text = readFile(text_file)
	annotation_ann = readFile(annotation_file)

	id = computeID(text,user)

	wordsCount = fileProcesser.readText(text_file)

	tokensDic = {}
	tokenIndex = {}
	relations = []
	predicationsDic = {}

	with open(annotation_file,'r') as f:
		content = f.read()
	lines = content.split('\n')
	for i in range(len(lines)-1): ##aviod last line, where has noting
		splitedLine=lines[i].split('\t')
		index = splitedLine[0]

		if(index[0]=='T'):###tokens
			token = splitedLine[2]
			tokenConverted = token.title()
			tokenIndex[index] = token
			if token in tokensDic.keys():
				num = tokensDic[token] +1
				tokensDic[token] = num
			else:
				tokensDic[token] = 1
		else:
			relation = splitedLine[1].split(' ')[0]
			Arg1Index = splitedLine[1].split(' ')[1].split(":")[1]
			Arg2Index = splitedLine[1].split(' ')[2].split(":")[1]
			relations.append({"relation":relation,"Arg1":Arg1Index,"Arg2":Arg2Index})

	for item in relations:
		arg1 = tokenIndex[item["Arg1"]]
		arg2 = tokenIndex[item["Arg2"]]
		relation = item["relation"]

		if arg1+relation in predicationsDic.keys():
			num = predicationsDic[arg1+relation]
			predicationsDic[arg1+relation] = num
		else:
			predicationsDic[arg1+relation] = 1

		if relation+arg2 in predicationsDic.keys():
			num = predicationsDic[relation+arg2]
			predicationsDic[relation+arg2] = num
		else:
			predicationsDic[relation+arg2] = 1

		if arg1+relation+arg2 in predicationsDic.keys():
			num = predicationsDic[arg1+relation+arg2]
			predicationsDic[arg1+relation+arg2] = num
		else:
			predicationsDic[arg1+relation+arg2] = 1	


	doc1 = {"text":text,"annotation":annotation_ann}
	doc2 = {"tokens":tokensDic,
			"predications":predicationsDic,
			"wordsCount":wordsCount}

	fileDatabase = server[db]
	searchDatabase = server[db+"search"]

	fileDatabase[id] = doc1
	searchDatabase[id] = doc2




# def save_annotated_text(db,text_file,user,annotation_file):
# 	##save text into couchdb 
# 	text = readFile(text_file)
# 	annotation_ann = readFile(annotation_file)


# 	id = computeID(text,user)

# 	wordCount = fileProcesser.readText(text_file)
# 	tokens,relations,predications,partitions = fileProcesser.readAnnotation(annotation_file)
# 	tree,tokensNotInTree = fileProcesser.saveInTree(tokens)

# 	_doc ={
# 		"_id":id,
# 		"annotater":user,
# 		"text":text,
# 		"annotation":annotation_ann,
# 		"predications" : predications,
# 		"Anatomy" : partitions[0],
# 		"Organisms" : partitions[1],
# 		"Diseases" : partitions[2],
# 		"Chemicals_and_Drugs" : partitions[3],
# 		"Analytical_Diagnostic_and_Therapeutic_Techniques_and_Equipment" : partitions[4],
# 		"Psychiatry_and_Psychology" : partitions[5],
# 		"Phenomena_and_Processes" : partitions[6],
# 		"Disciplines_and_Occupations" : partitions[7],
# 		"Anthropology_Education_Sociology_and_Social_Phenomena" : partitions[8],
# 		"Technology_Industry_Agriculture" : partitions[9],
# 		"Humanities" : partitions[10],
# 		"Information_Science" : partitions[11],
# 		"Named_Groups" : partitions[12],
# 		"Health_Care" : partitions[13],
# 		"Publication_Characteristics" : partitions[14],
# 		"Geographicals" : partitions[15],
# 		"otherTokens" : partitions[16],
# 		"tokens" : tokens,
# 		"Relations" : relations,
# 		"wordCount" : wordCount

# 	} 

# 	##connect to databse
# 	db = server.database(db)

# 	db.save(_doc)


############################################################################################################################
######  only create a view if there needs a new one or the map_reduce function have been updated      ######################
######              use query if you just want to get your data from an exist view !!!                ######################
############################################################################################################################

def create_view(db,map,reduce,key):

	#create view with provided map and reduce function 

	#pass http://username:password@ip_address:5984/ to server constructor:
	couchdb = server.database(db)

	#the view_name must be  map + reduce
	view_name = map + reduce

	# get the path of map function and read it
	map_dir=os.path.abspath('.')+"/map_reduce_function/"+map+".js"
	map_func = open(map_dir).read()
	#print (map_func)


	#not grouped as default
	group = 'false'

	#design view
	if reduce == '':
		_doc= {
    		"_id" : "_design/"+view_name,
    		"views" : {
    			key:{
    				"map" : map_func,
    			}
    		}
    	}
		#print (_doc)
	else:
		group = 'true'
		if reduce in "_sum _count _stats":
			reduce_func = reduce
		else:
			reduce_dir = os.path.abspath('.')+"/map_reduce_function/"+reduce+".js"
			reduce_func = open(reduce_dir).read()
		_doc= {
    		"_id" : "_design/"+view_name,
    		"views" : {
    			key:{
    				"map" : map_func,
    				"reduce" : reduce_func,
    			}
    		}
    	}
		#print (_doc)

	#create view 	
	if "_design/"+view_name in couchdb:
		#view already there，delete and re-create in case function has benn modified
		couchdb.delete("_design/"+view_name)
		doc = couchdb.save(_doc)
		#print("view already exist")
	else:
		# create a view if its not there 
		doc = couchdb.save(_doc)

	
	##return :      db     : the name of database where you create your biew
	##			view_name  : map+reduce, which can be used to query your view
	##				key    : just "id_str" the most time in our design
	##			   group   : group is true if reduce function is used    		
	return {"db":couchdb,"view_name":view_name,"key":key,"group":group}

	
def databaseCount(db):
	## db = "demo8search"
	database = server[db]
	databaseWordsCount = 0
	for row in database.view("_all_docs"):
		print(row.id)
		if database[row.id]["wordsCount"] != null:
			databaseWordsCount = databaseWordsCount + database[row.id]["wordsCount"]
	info = database.info()
	docsCount = info["doc_count"]

	today=datetime.date.today()

	database[str(today)] = {"databaseDocsCount":docsCount,"databaseWordsCount":databaseWordsCount}