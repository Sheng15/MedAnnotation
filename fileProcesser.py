from treelib import Node, Tree
import sys
import os

import meshTree

class Token(object):
	def __init__(self,tag,start,end):
		self.tag = tag
		self.start = start
		self.end = end

def readAnnotation(file):
	##T1\tDrug 1000 1025\tanticoagulant medications\nT2\tDrug 3620 3628\tdilaudid\n
	##R1\tRoute-Drug Arg1:T3 Arg2:T2
	A = []
	B = []
	C = []
	D = []
	E = []
	F = []
	G = []
	H = []
	I = []
	J = []
	K = []
	L = []
	M = []
	N = []
	V = []
	Z = []
	otherToken = []
	tokens = [] 
	relations = list()
	predications = list()
	with open(file,'r') as f:
		content = f.read()
	lines = content.split('\n')
	for i in range(len(lines)-1): ##aviod last line, where has noting
		splitedLine=lines[i].split('\t')
		index = splitedLine[0]

		if(index[0]=='T'):###tokens
			category=splitedLine[1].split(' ')[0]
			start = splitedLine[1].split(' ')[1]
			end = splitedLine[1].split(' ')[2]
			token = splitedLine[2]
			tokenConverted = token.title()
			if meshTree.containsToken(tokenConverted):
				nids = meshTree.meshDic[tokenConverted]			
				if  ('A' in nids[0]):
					A.append(token)
				elif('B' in nids[0]):
					B.append(token)
				elif('C' in nids[0]):
					C.append(token)
				elif('D' in nids[0]):
					D.append(token)
				elif('E' in nids[0]):
					E.append(token)
				elif('F' in nids[0]):
					F.append(token)
				elif('G' in nids[0]):
					G.append(token)
				elif('H' in nids[0]):
					H.append(token)
				elif('I' in nids[0]):
					I.append(token)
				elif('J' in nids[0]):
					J.append(token)
				elif('K' in nids[0]):
					K.append(token)
				elif('L' in nids[0]):
					L.append(token)
				elif('M' in nids[0]):
					M.append(token)
				elif('N' in nids[0]):
					N.append(token)
				elif('V' in nids[0]):
					V.append(token)
				else:
					Z.append(token)
			else:
				otherToken.append(token)
			tokens.append({"index":index,"category":category,"start":start,"end":end,"token":token})
		else:
			relation = splitedLine[1].split(' ')[0]
			Arg1 = splitedLine[1].split(' ')[1]
			Arg2 = splitedLine[1].split(' ')[2]
			relations.append({"index":index,"relation":relation,"Arg1":Arg1,"Arg2":Arg2})
			if relation not in predications:
				predications.append(relation)
	f.close()
	partitions = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,V,Z,otherToken]
	return tokens,relations,predications,partitions

def readText(file):
	wordCount = 0
	with open(file, 'r') as f:
		content = f.read()
	lines = content.split('\n')
	for line in lines:
		words = line.split()
		wordCount += len(words)
	f.close()
	return wordCount

def containsList(tree,nids):
	for nid in nids:
		if tree.contains(nid):
			return True	
	return False

def saveInTree(tokens):
	tokensNotInTree = []
	tree = Tree()
	tree.create_node('Root','root')##root

	for token in tokens:
		tokenConverted = token['token'].title()
		if meshTree.containsToken(tokenConverted):##containsToken(token)
			##print(tokenConverted)
			nids = meshTree.meshDic[tokenConverted]
			if(containsList(tree,nids)):
				leaf = Node(token["token"],token["index"],data = [token["index"],token["category"],token["start"],token["end"]])
				tree.add_node(leaf,'root')
			else:
				ancestorsList = meshTree.getAncestors(tokenConverted)
				for ancestors in ancestorsList:
					for i in range(len(ancestors)-1):
						if(not(tree.contains(ancestors[i]))):##contains(nid)
							node = Node(meshTree.getTag(ancestors[i]),ancestors[i])
							parent = ancestors[i-1]
							tree.add_node(node,parent)
					leaf = Node(token["token"],ancestors[-1],data = [token["index"],token["category"],token["start"],token["end"]])
					tree.add_node(leaf,ancestors[-2])
		else:
			tokensNotInTree.append(token)

	return tree,tokensNotInTree



