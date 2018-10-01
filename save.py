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

def save_annotated_text(db,text_file,user,annotation_file):
	##save text into couchdb 

	text = readFile(text_file)
	annotation_ann = readFile(annotation_file)


	id = computeID(text,user)

	annotation = dp.readAnnotation(annotation_file)

	tokens = annotation[0]
	trees= dp.tree_of_tokens(tokens)
	tree_of_chemicals=trees[0].to_dict()
	tree_of_diseases=trees[1].to_dict()
	tree_of_genes=trees[2].to_dict()

	_doc ={
		"_id":id,
		"annotater":user,
		"text":text,
		"annotation":annotation_ann,
		"Chemicals": tree_of_chemicals,
		"Diseases" : tree_of_diseases,
		"Genes" : tree_of_genes,
		"Relations" : annotation[1],
		"count" : annotation[2]
	} 

	##connect to databse
	db = server.database(db)

	db.save(_doc)

def save():
	for i in range(1,70000):
		text_file = "data/"+str(i)+".txt"
		annotation_file = "data/"+str(i)+".ann"
		db = "demo2"
		user = 'Tom'
		save_annotated_text(db,text_file,user,annotation_file)




		