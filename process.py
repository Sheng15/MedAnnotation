import couchdb
import json
import sys
import os
import mmh3


server = couchdb.Server('http://admin:admin@localhost:5984/')


def readFile(file):
	f = open(file,'r')
	result = ''
	for line in f.readlines():
		result = result+line
	f.close()
	return result


def get_text_all(db,text_file):

	db = server[db]

	text = readFile(text_file)

	start_key= str(mmh3.hash(text,signed=False))
	end_key = start_key +"ZZZZZZZZZZ"

	result = list()
	for item in db.view('_all_docs', startkey=start_key, endkey=end_key):
		result.append(item.key)
	return result