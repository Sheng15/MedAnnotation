'''
define the hierarchy of the category.
both the category and the hierarchy may varies in different project.
in this project, we just define a simple hierachy of category as an example
'''
'''
CATEGORY = {
			Disease;A01,
			Neoplasms;A01.001,
			Cysts;A01.001.001
			Hamartoma;A01.001.002
			Infection;A01.002,
			Coinfection;A01.002.001,
			Sepsis,A01.002.002,
			Toxemia,A01.002.003,
			Chemicals;B01,
			Lipids;B01.001;
			Glycerides,B01.001.001;
			Natuderm,B01.001.002;
}
'''
def getDescendants(token,distance = False):
	'''
	some hard code to make it running
	further work required
	'''
	if distance == False:
		if token.lower() == "disease":
			return ["disease","neoplasms","cysts","hamartoma",
					"infection","coinfection","sepsis","toxemia"]
		elif token.lower() == "neoplasms":
			return ["neoplasms","cysts","hamartoma"]
		elif token.lower() == "infection":
			return ["infection","coinfection","sepsis","toxemia"]
		elif token.lower() == "chemicals":
			return ["chemicals","lipids","glycerides","natuderm"]
		else:
			return []
	else:
		if token.lower() == "disease":
			return {"disease":0,"neoplasms":1,"cysts":2,"hamartoma":2,
					"infection":1,"coinfection":2,"sepsis":2,"toxemia":2}
		elif token.lower() == "neoplasms":
			return {"neoplasms":0,"cysts":1,"hamartoma":1}
		elif token.lower() == "infection":
			return {"infection":0,"coinfection":1,"sepsis":1,"toxemia":1}
		elif token.lower() == "chemicals":
			return {"chemicals":0,"lipids":1,"glycerides":1,"natuderm":1}
		else:
			return {}