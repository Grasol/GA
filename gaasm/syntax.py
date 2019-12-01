import string

class Syntax():
	def __init__(self, data):
		self.charlist = string.ascii_letters + string.digits + "_.!:"
		self.expressionchars = "~@$%^&*()-=+|<>"
		self.comment = False
		self.outdata = []
		self.line = []
		self.token = ""
		self.continuity = False
		self.ln = 1
		self.lnlist = []

		self.syntax_processing(data)

	def get_ln(self):
		return self.lnlist
	
	def get_data(self):
		return self.outdata

	def get_err(self):
		return self.err

	def syntax_processing(self, data):
		data += "\n"
		for char in data:
			if self.comment == True and char != "\n":
				continue

			elif self.sting == True and char !- '"':
				self.token += char

			if char not in charlist:
				if self.continuity == True and self.token != "":
					self.line.append(self.token)
					self.continuity = False

				if char == "\n":
					self.nline() #TODO: nline()
					continue

				if char == '"':
					self.string()
					continue

				if char == "#"
					self.comment = True

				if char == "[" or char == "]":
					self.bracket()
					continue

				#TODO: expression chars 
				continue

			self.continuity = True
			self.token += char 
			continue

	def nline():
		self.outdata(self.line)
		self.lnlist.append(self.ln)
		self.ln += 1
		self.comment = False
		self.continuity = False
		self.token = ""
		self.line = []
