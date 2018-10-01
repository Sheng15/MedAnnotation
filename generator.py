import os
import random

Category = ["Chemicals","Diseases","Genes"]

Chemicals = ["chemicals","amino acids","carbohydrates","cleonine","desmopyridine","carbasugars","sugar acids","gluconates","calcium gluconate","sanasol"]

Diseases = ["diseases","eye diseases","neoplasms","asthenopia","glaucoma","cysts","hamartoma"]

Genes = ["genes","a3226_GR01","a3226_GT04","a3226_GT14","a3230_GT11","a3235_GT02"]

Relations = ["treat","cause","influence"]

text = ["Chemicals","Diseases","Genes","chemicals","amino acids","carbohydrates","cleonine","desmopyridine",
		"carbasugars","sugar acids","gluconates","calcium gluconate","sanasol","diseases","eye diseases",
		"neoplasms","asthenopia","glaucoma","cysts","hamartoma","genes","a3226_GR01","a3226_GT04","a3226_GT14",
		"a3230_GT11","a3235_GT02","treat","cause","influence"]


def ge():
	##T1\tDrug 1000 1025\tanticoagulant medications\nT2\tDrug 3620 3628\tdilaudid\n
	##R1\tRoute-Drug Arg1:T3 Arg2:T2
	for i in range(50000):
		file ="data/"+str(i)+".ann"
		f = open(file,'w')
		myCate = random.randint(0,2)
		if(myCate==0):
			tokenCount = random.randint(1,80)
			for k in range(tokenCount):
				tag="T"+str(k)
				token = Chemicals[random.randint(0,9)]
				line=tag+"\t"+"Chemicals 0 0\t"+token+'\n'
				f.write(line)
		elif(myCate==1):
			tokenCount = random.randint(1,80)
			for k in range(tokenCount):
				tag="T"+str(k)
				token = Diseases[random.randint(0,6)]
				line=tag+"\t"+"Diseases 0 0\t"+token+'\n'
				f.write(line)
		else:
			tokenCount = random.randint(1,80)
			for k in range(tokenCount):
				tag="T"+str(k)
				token = Genes[random.randint(0,5)]
				line=tag+"\t"+"Genes 0 0\t"+token+'\n'
				f.write(line)

		for i in range(random.randint(1,20)):
			tag = "R"+str(i)
			Arg1="T"+str(random.randint(0,tokenCount))
			Arg2="T"+str(random.randint(0,tokenCount))
			line = tag+"\t"+Relations[random.randint(0,2)]+" Arg1:"+Arg1+" Arg2:"+Arg2+'\n'
			f.write(line)
		f.close()


def ge2():
	for i in range(50000,70000):
		file ="data/"+str(i)+".ann"
		f = open(file,'w')
		tokenCount = random.randint(1,80)
		for i in range(tokenCount):
			tag="T"+str(i)
			myCate = random.randint(0,2)
			if(myCate==0):
				token = Chemicals[random.randint(0,9)]
				line=tag+"\t"+"Chemicals 0 0\t"+token+'\n'
				f.write(line)
			elif(myCate==1):
				token = Diseases[random.randint(0,6)]
				line=tag+"\t"+"Diseases 0 0\t"+token+'\n'
				f.write(line)
			else:
				token = Genes[random.randint(0,5)]
				line=tag+"\t"+"Genes 0 0\t"+token+'\n'
				f.write(line)
		for i in range(random.randint(1,20)):
			tag = "R"+str(i)
			Arg1="T"+str(random.randint(0,tokenCount))
			Arg2="T"+str(random.randint(0,tokenCount))
			line = tag+"\t"+Relations[random.randint(0,2)]+" Arg1:"+Arg1+" Arg2:"+Arg2+'\n'
			f.write(line)
		f.close()

def ge3():
	for i in range(70000):
		file ="data/"+str(i)+".txt"
		f = open(file,'w')
		wordCount = random.randint(10,200)
		for i in range(wordCount):
			token = text[random.randint(0,28)]
			f.write(token)
		f.close()

