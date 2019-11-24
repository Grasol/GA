

class Syntax():
	def __init__(self, data):
		syx = syntax_processing(data)
		self.procdata = syx[0]
		self.lnlist = syx[1]
		self.err = syx[2]

	def get_ln(self):
		return self.lnlist
	
	def get_data(self):
		return self.procdata

	def get_err(self):
		return self.err

def syntax_processing(data):
	data += "\n"
	procdata = []
	ln = 1
	lnlist = []
	a = ""
	commentloop = False
	parenthesis = 0
	err = []

	for d in data:
		if commentloop == True and d != "\n":
			continue
	
		if d == "[" and parenthesis == 0 or d == "[" and parenthesis == 1:
			parenthesis += 1
			a += " [ "
			continue
		elif d == "[" and parenthesis >= 2:
			err.append("Error in line %i: bad syntax: '['" %ln)
	
		if d == "]" and parenthesis == 1 or d == "]" and parenthesis == 2:
			parenthesis -= 1
			a += " ] "
			continue
		elif d == "]" and parenthesis <= 0:
			err.append("Error in line %i: bad syntax: ']'" %ln)
	
		if d == "," or d == "+":
			a += " %c "%d
			continue
	
		if d == "\n":
			if parenthesis > 0:
				err.append("Error in line %i: don't close parenthesis"%ln)

			if a != "" and parenthesis == 0:
				lnlist.append(ln)
				procdata.append(a)
			
			commentloop = False
			parenthesis = 0
			a = ""
			ln += 1
			continue
	
		if d == "#":
			commentloop = True
			continue
	
		a += d
	return (procdata, lnlist, err)

