import string

class Syntax():
	def __init__(self, data):
		self.outdata = []
		self.line = []
		self.lines = []
		self.token = ""
		self.ln = 1
		self.lnlist = []
		self.specialtoken = 0
		self.addrtoken = 0
		self.strtoken = 0
		self.endtoken = 0
		
		self.syntax_processing(data)


	def get_ln(self):
		return self.lnlist

	
	def get_data(self):
		return self.lines 


	def get_err(self):
		#return self.err
		pass


	def syntax_processing(self, data):
		data += "\n"
		self.token = ""
		self.check_f_t = 0
		self.check_a_t = 0
		self.comment = False

		for char in data:
			if char == ";" and self.comment == False:
				char = "\n"
				self.ln -= 1

			if self.comment == True and char != "\n":
				continue

			if self.check_f_t != 2:
				self.first_token(char)
				continue

			if self.check_f_t == 2:
				self.arg_token(char)


	def first_token(self, char):
		if char not in string.whitespace:
			self.thisln = self.ln
			self.check_f_t = 1
			"""if char == ":":
				self.line.append(":")
				return"""

			if char == "#":
				self.comment = True
				return
	
			self.token += char
			return

		if self.check_f_t == 1:
			self.check_f_t = 2
			self.line.append(self.token)
			self.token = ""
			
		if char == "\n":
			if len(self.line) != 0:
				if len(self.line[0]) != 0:
					self.lines.append(self.line)
					self.lnlist.append(self.thisln)
			
			self.line = []
			self.token = ""
			self.check_f_t = 0
			self.comment = False
			self.ln += 1
			return


	def arg_token(self, char): #please, you don't touch "if"s
		if char == "#" and self.strtoken != 1:
			self.comment = True
			return

		if char == '"' or self.strtoken == 1:
			self.check_a_t = 1
			self.string_token(char)
			return
			
		if char == ",":
			self.line.append(self.token)
			self.token = ""
			self.check_a_t = 0
			return

		if char not in string.whitespace and (self.check_a_t == 1 or self.check_a_t == 0):
			self.check_a_t = 1
			self.token += char
			return

		if char == "\n":
			if self.token != "":
				self.line.append(self.token)
			
			if len(self.line) != 0: 
				self.lnlist.append(self.thisln)
				self.lines.append(self.line)

			self.token = ""
			self.line = []
			self.check_a_t = 0
			self.check_f_t = 0
			self.comment = False
			self.ln += 1
			return

		if self.check_a_t == 1:
			self.check_a_t = 2
			return

	"""def address_token(self, char):
		self.specialtoken = 2
		if char in string.whitespace:
			return ""

		if char == "[":
			self.addrtoken += 1
		if self.addrtoken > 2:
			#TODO err
			pass

		if char == "]":
			self.addrtoken -= 1
		if self.addrtoken == 0:
			self.specialtoken = 0

		return char"""


	def string_token(self, char):
		if char == '"':
			self.strtoken += 1

		if char == "\n":
			self.ln += 1

		if self.strtoken == 2:
			self.strtoken = 0
			self.check_a_t = 2

		self.token += char


