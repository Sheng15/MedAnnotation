from treelib import Node, Tree
import meshTree

meshTree,meshDic = meshTree.loadMeshTree()
		

def notRoot(tree,nid):
	if(nid==tree.root):
		return False
	else:
		return True



def getAncestors(token):
	ancestorsList=[]

	if (token in meshDic.keys()):
		nids = meshDic[token]
		for nid in nids:
			ancestors = []	
			while(notRoot(meshTree,nid)):
				nid = meshTree.parent(nid).identifier
				ancestors.append(nid)
			ancestors = list(reversed(ancestors))
			ancestorsList.append(ancestors)
	else:
		print("cannot find "+token+" in the MeSH!")

	return ancestorsList






	


	