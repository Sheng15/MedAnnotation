from treelib import Node, Tree


TREE_PATH = "mtrees2018.bin"

CATAGORY = ["Anatomy","Organisms","Diseases","Chemicals and Drugs","Analytical, Diagnostic and Therapeutic Techniques and Equipment","Psychiatry and Psychology","Phenomena and Processes","Disciplines and Occupations",
"Anthropology, Education, Sociology and Social Phenomena","Technology, Industry, Agriculture","Humanities","Information Science","Named Groups","Health Care","Publication Characteristics","Geographicals"]
'''
A. Anatomy
B. Organisms
C. Diseases
D. Chemicals and Drugs
E. Analytical, Diagnostic and Therapeutic Techniques and Equipment
F. Psychiatry and Psychology
G. Phenomena and Processes
H. Disciplines and Occupations
I. Anthropology, Education, Sociology and Social Phenomena
J. Technology, Industry, Agriculture
K. Humanities 
L. Information Science 
M. Named Groups
N. Health Care
V. Publication Characteristics 
Z. Geographicals
'''

def readTree(TREE_PATH):
	tokens = []

	with open(TREE_PATH,'rb') as f:
		data = f.read()
		contents = data.decode('utf-8').split('\n')

	for content in contents:
		token = content.split(';')
		tokens.append(token)
	return tokens[:-1]

def creatTree(tokens):
	meshTree = Tree()

	meshTree.create_node('Root','root')##root
	for category in CATAGORY:
		meshTree.create_node(category,category,parent = 'root')##initial the tree

	for token in tokens:
		if(not'.' in token[1]): ## tokens with ids like 'A01' that are the elder sons of each category
			if  ('A' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Anatomy')
			elif('B' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Organisms')
			elif('C' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Diseases')
			elif('D' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Chemicals and Drugs')
			elif('E' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Analytical, Diagnostic and Therapeutic Techniques and Equipment')
			elif('F' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Psychiatry and Psychology')
			elif('G' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Phenomena and Processes')
			elif('H' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Disciplines and Occupations')
			elif('I' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Anthropology, Education, Sociology and Social Phenomena')
			elif('J' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Technology, Industry, Agriculture')
			elif('K' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Humanities')
			elif('L' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Information Science')
			elif('M' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Named Groups')
			elif('N' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Health Care')
			elif('V' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'Publication Characteristics')
			else:
				meshTree.create_node(token[0],token[1],parent = 'Geographicals')
		else:
			parent_id = token[1][:-4]
			meshTree.create_node(token[0],token[1],parent= parent_id)
	return meshTree

def createDictionary(tokens):
	dic = {}

	for token in tokens:
		current_id = []
		token_str = token[0]
		token_id = token[1]
		if (token_str not in dic.keys()):
			current_id.append(token_id)
			dic[token_str] = current_id
		else: 
			dic[token_str].extend([token_id])
			dic[token_str] = dic[token_str]
	return dic


def loadMeshTree():
	tokens = readTree(TREE_PATH)			
	meshTree = creatTree(tokens)
	meshDic = createDictionary(tokens)
	return meshTree,meshDic


##################################################################################
meshTree,meshDic = loadMeshTree()

def notRoot(nid):
	if(nid==meshTree.root):
		return False
	else:
		return True

def containsToken(token):
	if token in meshDic.keys():
		return True
	else:
		return False

def getTag(nid):
	return meshTree.get_node(nid).tag

def getnids(token):
	if (containsToken(token)):
		nids = meshDic[token]
	return nids

def getAncestors(token):
	ancestorsList=[]

	if (containsToken(token)):
		nids = meshDic[token]
		for nid in nids:
			ancestors = [nid]	
			while(notRoot(nid)):
				nid = meshTree.parent(nid).identifier
				ancestors.append(nid)
			ancestors = list(reversed(ancestors))
			ancestorsList.append(ancestors)
	else:
		print("cannot find "+token+" in the MeSH!")

	return ancestorsList


def getDescendants(token,distance = False):
	if distance == False:
		descendants = []
		if (containsToken(token)):
			nids = meshDic[token]
			for nid in nids:
				subTree = meshTree.subtree(nid)
				allNodes = subTree.all_nodes()
				for node in allNodes:
					if node.tag in descendants:
						pass
					else: 
						descendants.append(node.tag)
		return descendants
	else:
		descendants = {}
		if (containsToken(token)):
			nids = meshDic[token]
			for nid in nids:
				subTree = meshTree.subtree(nid)
				allNodes = subTree.all_nodes()
				for node in allNodes:
					if node.tag in descendants.keys():
						if subTree.level(node.identifier) < descendants[node.tag]:
							descendants[node.tag] = subTree.level(node.identifier)
						else:
							pass
					else:
						descendants[node.tag] = subTree.level(node.identifier)
		return descendants





def getTokenAncestors(token):
	ancestorsList=[]

	if (containsToken(token)):
		nids = meshDic[token]
		for nid in nids:
			ancestors = []	
			while(notRoot(nid)):
				parent = meshTree.parent(nid)
				ancestors.append(parent.tag)
				nid = parent.identifier
			ancestors = list(ancestors[:-2])
			ancestorsList.append(ancestors)
	else:
		print("cannot find "+token+" in the MeSH!")

	return ancestorsList
