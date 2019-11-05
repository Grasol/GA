class Syntax():
	def __init__(self, data):
		syx = syntax_processing(data)
		self.procdata = syx[0]
		self.lnlist = syx[1]

	def get_ln(self):
		return self.lnlist
	
	def get_data(self):
		return self.procdata

def syntax_processing(data):
	data += "\n"
	procdata = []
	ln = 1
	lnlist = []
	a = ""
	commentloop = False
	parenthesis = False
	
	for d in data:
		if commentloop == True and d != "\n":
			continue
	
		if d == "[" and parenthesis == False:
			parenthesis = True
			a += " [ "
			continue
		elif d == "[" and parenthesis == True:
			print("Error in line %i: bad syntax: '['" %ln)
	
		if d == "]" and parenthesis == True:
			parenthesis = False
			a += " ] "
			continue
		elif d == "]" and parenthesis == False:
			print("Error in line %i: bad syntax: ']'" %ln)
	
		if d == "," or d == "+":
			a += " "
			a += d
			a += " "
			continue
	
		if d == "\n":
			if a != "":
				lnlist.append(ln)
				procdata.append(a)
			
			commentloop = False
			a = ""
			ln += 1
			continue
	
		if d == "#":
			commentloop = True
			continue
	
		a += d
	return (procdata, lnlist)

