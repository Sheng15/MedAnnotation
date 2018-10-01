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
	tokens =list()
	relations = list()
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
			tokens.append({"index":index,"category":category,"start":start,"end":end,"token":splitedLine[2]})
		else:
			relation = splitedLine[1].split(' ')[0]
			Arg1 = splitedLine[1].split(' ')[1]
			Arg2 = splitedLine[1].split(' ')[2]
			relations.append({"index":index,"relation":relation,"Arg1":Arg1,"Arg2":Arg2})
	f.close()
	return tokens,relations

	

def saveInTree(tokens):
	tokensNotInTree = []
	tree = Tree()
	tree.create_node('Root','root')##root

	for token in tokens:
		if meshTree.containsToken(token["token"]):##containsToken(token)
			ancestorsList = meshTree.getAncestors(token["token"])
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

