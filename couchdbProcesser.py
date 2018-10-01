##author Sheng Tang
##08/05/2018  16:40

##library used is py-couchdb from https://github.com/histrio/py-couchdb
##Document can be find at https://pycouchdb.readthedocs.org/



######################################################################################################
#############	general methods that can be invoked to perform basic database process    ############# 
#############	inclouding：query view，query a grouped view，obtain data，save file     #############
#############                or data into couchdb. And a method to create view           #############
###################################################################################################### 
#python3

import pycouchdb
import json
import sys
import os
import mmh3
import dictProcesser as dp 

from treelib import Node, Tree


##connect to database, "admin" as the user name and password to make our life easier
server = pycouchdb.Server('http://admin:admin@localhost:5984/')
#server = pycouchdb.Server('http://localhost:5984/')




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

	db = server.database(db)

	text = readFile(text_file)
	id = computeID(text,user)

	doc = db.get(id)
	return doc


def get_text_all(db,text_file):
	text = readFile(text_file)

	text_id = computeID(text,user)

	start_key= text_id
	end_key = text_id +"ZZZZZZZZZZ"




def query_view(db,viewName):

	##connect to databse
	db = server.database(db)

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


def get_data(db,dataname):

	##connect to databse
	db = server.database(db)

	# get data
	result=db.get(dataname)

	return result


def save_file(db,file):
	#save json file into couchdb

	##connect to databse
	db = server.database(db)

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
	db = server.database(db)

	db.save(_doc)


def save_annotated_text(db,text_file,user,annotation_file):
	##save text into couchdb 

	text = readFile(text_file)
	annotation_ann = readFile(annotation_file)


	id = computeID(text,user)

	annotation = dp.readAnnotation

	trees= dp.tree_of_tokens(annotation[0])
	tree_of_chemicals=trees[0].to_dict(with_data=True)
	tree_of_diseases=trees[1].to_dict(with_data=True)
	tree_of_genes=trees[2].to_dict(with_data=True)

	_doc ={
		"_id":id,
		"annotater":user,
		"text":text,
		"annotation":annotation_ann
		"Chemicals": tree_of_chemicals
		"Diseases" : tree_of_diseases
		"Genes" : tree_of_genes
		"Relations" : annotation[1]
		"count" : annotation[2]
	} 

	##connect to databse
	db = server.database(db)

	db.save(_doc)


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

	
