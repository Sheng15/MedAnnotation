from treelib import Node, Tree

Category = ["Chemicals","Diseases","Genes"]

Chemicals = Tree()
Diseases = Tree()
Genes = Tree()

def initial():
	Chemicals.create_node("Chemicals","chemicals") ##root
	Chemicals.create_node("Amino Acids","amino acids",parent="chemicals")
	Chemicals.create_node("Carbohydrates","carbohydrates",parent="chemicals")
	Chemicals.create_node("Cleonine","cleonine",parent="amino acids")
	Chemicals.create_node("Desmopyridine","desmopyridine",parent="amino acids")
	Chemicals.create_node("Carbasugars","carbasugars",parent="carbohydrates")
	Chemicals.create_node("Sugar Acids","sugar acids",parent="carbohydrates")
	Chemicals.create_node("Gluconates","gluconates",parent="sugar acids")
	Chemicals.create_node("Calcium Gluconate","calcium gluconate",parent="gluconates")
	Chemicals.create_node("Sanasol ","sanasol",parent="calcium gluconate")



	Diseases.create_node("Diseases","diseases") ##root
	Diseases.create_node("Eye Diseases","eye diseases",parent="diseases")
	Diseases.create_node("Neoplasm","neoplasms",parent="diseases")
	Diseases.create_node("Asthenopia","asthenopia",parent="eye diseases")
	Diseases.create_node("Glaucoma","glaucoma",parent="eye diseases")
	Diseases.create_node("Cysts","cysts",parent="neoplasms")
	Diseases.create_node("Hamartoma","hamartoma",parent="neoplasms")


	Genes.create_node("Genes","genes") ##root
	Genes.create_node("A3226_GR01","a3226_GR01",parent="genes")
	Genes.create_node("A3226_GT04","a3226_GT04",parent="genes")
	Genes.create_node("A3226_GT14","a3226_GT14",parent="genes")
	Genes.create_node("A3230_GT11","a3230_GT11",parent="genes")
	Genes.create_node("A3235_GT02","a3235_GT02",parent="genes")

def show():
	Chemicals.show()
	Diseases.show()
	Genes.show()

def get_tree(root):
	if(root=="Chemicals"):
		return Chemicals
	elif(root=="Diseases"):
		return Diseases
	elif(root=="Genes"):
		return Genes
	else:
		print("tree not found!")
