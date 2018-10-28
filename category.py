'''
define the hierarchy of the category.
both the category and the hierarchy may varies in different project.
in this project, we just define a simple hierachy of category as an example
'''

CATEGORY = {
			Disease;A01,
			Mentak Disorders;A01.001,
			Anxiety Disorders;A01.001.001
			Mood Disorders;A01.001.002
			Eye Disease;A01.002,
			Eye Injuries;A01.002.001,
			Asthenopia,A01.002.002,
			Ocular Hypotension,A01.002.003,
			Virus Disease;A01.003,
			Bronchiolitis, Viral;A01.003.001;
			Viremia,A01.003.002;
			Zoonoses,A01.003.003;
}

def getDescendants(token,distance = False):
	'''
	some hard code to make it running
	further work required
	'''
	if distance = False:
		if token.lower() == "disease":
			return ["mentak disorders","anxiety disorders","mood disorders",
					"eye disease","eye injuries","asthenopia","ocular hypotension",
					"virus disease","bronchiolitis, viral","viremia","zoonoses"]
		elif token.lower() == "mentak disorders":
			return ["anxiety disorders","mood disorders"]
		elif token.lower() == "eye disease":
			return ["eye injuries","asthenopia","ocular hypotension"]
		elif token.lower() == "virus disease":
			return ["bronchiolitis, viral","viremia","zoonoses"]
		else:
			return []
	else:
		if token.lower() == "disease":
			return {"mentak disorders":1,"anxiety disorders":2,"mood disorders":2,
					"eye disease":1,"eye injuries":2,"asthenopia":2,"ocular hypotension":2,
					"virus disease":1,"bronchiolitis, viral":2,"viremia":2,"zoonoses":2}
		elif token.lower() == "mentak disorders":
			return {"anxiety disorders":1,"mood disorders":1}
		elif token.lower() == "eye disease":
			return {"eye injuries":1,"asthenopia":1,"ocular hypotension":1}
		elif token.lower() == "virus disease":
			return {"bronchiolitis, viral":1,"viremia":1,"zoonoses":1}
		else:
			return {}