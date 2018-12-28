##author Sheng Tang
##15/09/2018  10：23

import sys
import os
import datetime
import meshTree
import mmh3
import couchdb


###########################################################################################################
#############				Methods that can be used to save file into database   ############# 
#############				inclouding：save raw file or process it for query     #############
###########################################################################################################
#python3

##################################################################################################
######################  methods to read clinical trials and annotation files  ####################
##################################################################################################


def readFile(file):
	'''
	read a file with the given path
	Parameters
	• file 	- path of the file to be read
	returns a string of the content in the target file
	'''
	f = open(file,'r')
	result = ''
	for line in f.readlines():
		result = result+line
	f.close()
	return result

def countWord(file):
	'''
	count the word of a given file
	Parameters
	• file 	- path of the file to be read
	returns a int as the word count 
	'''
	wordCount = 0
	with open(file, 'r') as f:
		content = f.read()
	lines = content.split('\n')##remove all “\n” symbols
	for line in lines:
		words = line.split()
		wordCount += len(words)
	f.close()
	return wordCount


def computeID(text,user):
	'''
	user mmh3 hash to compute an identifier of a clinical trial and its annotation
	Parameters
	• text 	- string content of a text
	• user 	- identifier of the user， usually the user name
	returns a string of number as the identifier
	'''
	text_id = str(mmh3.hash(text,signed=False))
	user_id = str(mmh3.hash(user,signed=False))
	id = text_id+user_id
	return id



##################################################################################################
######################  process and save clinical trials and annotation files  ###################
##################################################################################################
def updateDic(token,dic):
	'''
	update the appearance frequency dict，the dict is something like {"aspirin"：2，"dilaudid"：1}
	Parameters
	• token - the key of the dict to be updated
	• dic 	- the appearance frequency dict
	'''
	if token in dic.keys():
			num = dic[token] +1
			dic[token] = num
	else:
		dic[token] = 1

def save_annotated_text(server,user,db,clinical_trial,annotation_file):

	##T1\tDrug 1000 1025\tanticoagulant medications\nT2\tDrug 3620 3628\tdilaudid\n
	##R1\tRoute-Drug Arg1:T3 Arg2:T2

	####step1.compute identifier
	text = readFile(clinical_trial)
	annotation_ann = readFile(annotation_file)
	id = computeID(text,user)

	####step2.count word of clinical trial
	wordsCount = countWord(clinical_trial)


	###step3.process annotation file，save the frequency of appearance of category,token,relation into a dict
	tokensDic = {}
	tokenIndex = {}
	categoryDic = {}
	categoryIndex = {}
	relations = []
	predicationsDic = {}

	with open(annotation_file,'r') as f:
		content = f.read()
	lines = content.split('\n') ## every line in the annotation file
	for i in range(len(lines)-1): ##aviod last line, where has noting
		splitedLine=lines[i].split('\t')
		index = splitedLine[0]   ## T or R

		if(index[0]=='T'):###tokens
			## update the dict of category
			category = splitedLine[1].split(' ')[0].lower()
			categoryIndex[index.lower()] = category
			updateDic(category,categoryDic)
			## update the dict of tokens
			token = splitedLine[2].lower() ### transfer all character to lower case
			tokenIndex[index.lower()] = token
			updateDic(token,tokensDic)
		else:
			##relations
			relation = splitedLine[1].split(' ')[0].lower()
			Arg1Index = splitedLine[1].split(' ')[1].split(":")[1].lower()
			Arg2Index = splitedLine[1].split(' ')[2].split(":")[1].lower()
			relations.append({"relation":relation,"Arg1":Arg1Index,"Arg2":Arg2Index})


	#### for a relation in annotation file, such as "R8	Form-Drug Arg1:T16 Arg2:T15"
	#### translate the index of the token "Arg1:T16" to the particular token it indicates
	for item in relations:
		arg1 = tokenIndex[item["Arg1"]]
		arg2 = tokenIndex[item["Arg2"]]
		arg1Category = categoryIndex[item["Arg1"]]
		arg2Category = categoryIndex[item["Arg2"]]
		relation = item["relation"]
		#print([arg1Category,arg1,relation,arg2Category,arg2])

		predications = [arg1Category+relation,arg1Category+relation+arg2,arg1Category+relation+arg2Category,
						arg1+relation,arg1+relation+arg2,arg1+relation+arg2Category,
						relation+arg2,relation+arg2Category]

		for predicate in predications:
			updateDic(predicate,predicationsDic)


	date = datetime.date.today()

	####step4.generate the two documents body to be saved to database
	_doc1 = {
			"User":user,
			"Clinical_Trial":text,
			"Annotation":annotation_ann,
			"Date":str(date)
			}
			
	_doc2 = {
			"User":user,
			"Category":categoryDic,
			"Tokens":tokensDic,
			"Predications":predicationsDic,
			"WordsCount":wordsCount
			}

	####step5.save to database
	try:
		fileDatabase = server[db]
		searchDatabase = server[db+"search"]
		fileDatabase[id] = _doc1
		searchDatabase[id] = _doc2
	except Exception as e:
		print("Failed to save file "+clinical_trial)
		print(e)
	####step6.update stats
	try:
		stats = searchDatabase.get("stats")
		wordsCount = stats["WordsCount"] + 1
		docsCount = stats["DocsCount"] + 1
		stats["WordsCount"] = wordsCount
		stats["DocsCount"] = docsCount
		searchDatabase["stats"] = stats
	except Exception as e:
		print("Failed to update stats")
		print(e)
		

def save(server,user,path,db):
	folder = path+"/saved"
	if not os.path.exists(folder):
		os.makedirs(folder)
	else:
		pass

	mylist = os.listdir(path)
	for line in mylist:
		filepath = os.path.join(path, line)
		if os.path.isdir(filepath):
			print("dir:" + filepath)
		if os.path.isfile(filepath):
			if filepath[:-1] =="t":
				annotation_file = filepath[:-3]	+ ".ann"
				save_annotated_text(server,user,db,filepath,annotation_file)
