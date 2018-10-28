##author Sheng Tang
##15/09/2018  10：43

'''
process the mesh dictionary to a useable tree structure
for more detial of mesh, see "https://www.nlm.nih.gov/mesh/""
the document of treelib can be found at "https://treelib.readthedocs.io/en/latest/pyapi.html"
'''
from treelib import Node, Tree

'''
path of mesh.bin file download from "ftp://nlmpubs.nlm.nih.gov/online/mesh/2018/meshtrees/",which will be updated annually.
'''
TREE_PATH = "mtrees.bin"


'''
an enumerate of the categories in mesh(in lower case)
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
CATAGORY = ["anatomy","organisms","diseases","Cchemicals and drugs","analytical, diagnostic and therapeutic techniques and equipment","psychiatry and psychology","phenomena and processes","disciplines and occupations",
"anthropology, education, sociology and social phenomena","technology, industry, agriculture","humanities","information science","named groups","health care","publication characteristics","geographicals"]

#####################################################################
######################  construct the mesh tree  ####################
#####################################################################
def readTree():
	'''
	read the mesh tree from the TREE_PATH
	retruns an arrry of all the tokens in the mesh tree in lower case
	a token there is a list that include its term and its tree id 
	for example [["body regions,"a01"],[anatomic landmarks","a01.111]]
	'''
	tokens = []

	with open(TREE_PATH,'rb') as f:
		data = f.read()
		contents = data.decode('utf-8').split('\n')

	for content in contents:
		token = content.split(';').lower()
		tokens.append(token)
	return tokens[:-1]##the last token is null

def creatTree(tokens):
	'''
	construct a tree object of mesh tree, every node in the tree is a node object,
	wich has two attributes,nid and tag, refer treelib document for more info.
	nid refers to the treeid and tag refers to the term.
	Parameters
	• tokens - the tokens read from meshtree file
	retruns an tree object of mesh tree
	'''	
	meshTree = Tree()

	meshTree.create_node('Root','root')##root
	for category in CATAGORY:
		meshTree.create_node(category,category,parent = 'root')##initial the tree

	for token in tokens:
		if(not'.' in token[1]): ## tokens with ids like 'a01' that are the elder sons of each category
			if  ('a' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'anatomy')
			elif('b' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'organisms')
			elif('c' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'diseases')
			elif('d' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'chemicals and drugs')
			elif('e' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'analytical, diagnostic and therapeutic techniques and equipment')
			elif('f' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'psychiatry and psychology')
			elif('g' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'phenomena and processes')
			elif('h' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'disciplines and occupations')
			elif('i' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'anthropology, education, sociology and social phenomena')
			elif('j' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'technology, industry, agriculture')
			elif('k' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'humanities')
			elif('l' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'information science')
			elif('m' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'named groups')
			elif('n' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'health care')
			elif('v' in token[1]):
				meshTree.create_node(token[0],token[1],parent = 'publication characteristics')
			else:
				meshTree.create_node(token[0],token[1],parent = 'geographicals')
		else:
			parent_id = token[1][:-4]
			meshTree.create_node(token[0],token[1],parent= parent_id)
	return meshTree

def meshDict(tokens):
	'''
	create a dict object of mesh tree, some term in the tree might have multiple tree id
	for example {"term1":["treeid1","treeid2","treeid3"]}
	Parameters
	• tokens - the tokens read from meshtree file
	retruns a dict, keys are the terms in mesh with their treeids as value
	'''	
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
	'''
	use the methods above to load a mesh tree,
	returns a tree object and a dict object of mesh
	and you are ready to use mesh now!
	'''
	tokens = readTree(TREE_PATH)			
	meshTree = creatTree(tokens)
	meshDic = meshDict(tokens)
	return meshTree,meshDic


################################################################################## 
################### methods to use mesh tree and mesh dict########################
##################################################################################
meshTree,meshDic = loadMeshTree()

def notRoot(nid):
	'''
	check whether a node is the root of the meshtree
	Parameters
	• nid - the nid of a node
	retruns true if not root
	'''	
	if(nid==meshTree.root):
		return False
	else:
		return True

def containsToken(token):
	'''
	check whether a token can be found in meshtree
	Parameters
	• token - the token to be check
	retruns true if the token is found
	'''
	if token.lower() in meshDic.keys():
		return True
	else:
		return False

def getTag(nid):
	'''
	get the node's tag by its nid
	Parameters
	• nid - the nid of a node
	retruns tag of the node
	'''	
	return meshTree.get_node(nid).tag

def getnids(token):
	'''
	get the token's nids,it might more than one nid because a term might has multiple treeid
	Parameters	
	• token - the token to be check
	retruns a list of nids
	'''	
	if (containsToken(token)):
		nids = meshDic[token]
	return nids

def getAncestors(token):
	'''
	get the token's ancestors in mesh,there might be more than one nid,ancestors of each nid are expended
	Parameters	
	• token - the token to be check
	retruns a list of nids

	in this project, most time we dont care about the ancestors of a token. 
	'''	
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
	'''
	get the token's descendants in mesh,there might be more than one nid,decendants of each nid are expended
	Parameters	
	• token 	- the token to be check
	• distance  – (distance = False, not return the distance between a token and its descendants)
	for a hierarchy   A -> B -> C -> D,the distance would be {"A":0,"B":1,"C":2,"D":3}
	retruns a list of descendants

	in this project, use this method to support semantic search
	'''	
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

