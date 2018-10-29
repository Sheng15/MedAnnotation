import os
import random

import meshTree



text = ["Chemicals","Diseases","Genes","chemicals","amino acids","carbohydrates","cleonine","desmopyridine",
		"carbasugars","sugar acids","gluconates","calcium gluconate","sanasol","diseases","eye diseases",
		"neoplasms","asthenopia","glaucoma","cysts","hamartoma","genes","a3226_GR01","a3226_GT04","a3226_GT14",
		"a3230_GT11","a3235_GT02","treat","cause","influence"]

Category = ["disease","neoplasms","cysts","hamartoma","infection","coinfection","sepsis","toxemia",
			"chemicals","lipids","glycerides","natuderm"]

Relations = ["treat","cause","influence","Frequency-Drug","Duration-Drug","Strength-Drug","Route-Drug","Dosage-Drug","Form-Drug","Reason-Drug"]

mydict = meshTree.meshDic
myKeys = list(mydict.keys())


def ge():
	##T1\tDrug 1000 1025\tanticoagulant medications\nT2\tDrug 3620 3628\tdilaudid\n
	##R1\tRoute-Drug Arg1:T3 Arg2:T2
	tokenIndexs = []
	for i in range(2000):
		file ="data/"+str(i)+".ann"
		f = open(file,'w')
		tokenCount = random.randint(1,80)																		
		for k in range(tokenCount):
			tag="T"+str(k)
			cindex = random.randint(0,11)
			token = myKeys[random.randint(0,28936)]
			line=tag+"\t"+Category[cindex]+" 0 0\t"+token+'\n'
			f.write(line)


		for j in range(random.randint(1,20)):
			tag = "R"+str(j)
			Arg1="T"+str(random.randint(0,tokenCount-1))
			Arg2="T"+str(random.randint(0,tokenCount-1))
			line = tag+"\t"+Relations[random.randint(0,9)]+" Arg1:"+Arg1+" Arg2:"+Arg2+'\n'
			f.write(line)
		f.close()



def ge1():
	for i in range(2000):
		file ="data/"+str(i)+".txt"
		f = open(file,'w')
		wordCount = random.randint(10,200)
		for i in range(wordCount):
			token = text[random.randint(0,28)]
			f.write(token)
		f.close()

