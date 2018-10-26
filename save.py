import couchdb
import json
import sys
import os
import mmh3

import fileProcesser
from treelib import Node, Tree

##connect to database, "admin" as the user name and password to make our life easier
server = couchdb.Server('http://admin:admin@localhost:5984/')
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
	text = readFile(text_file)
	annotation_ann = readFile(annotation_file)

	id = computeID(text,user)

	wordsCount = fileProcesser.readText(text_file)+1000

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


def save():
	for i in range(239244,250000):
		print(i)
		text_file = "data/"+str(i)+".txt"
		annotation_file = "data/"+str(i)+".ann"
		db = "demo8"
		user = 'Tom'
		save_annotated_text(db,text_file,user,annotation_file)




		