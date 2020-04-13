import string

class Stream:
	def __init__(self, err, data):
		self.err = err
		self.data = data + "\n"

		self.i = -1
		self.istack = []

	def getChar(self):
		self.i += 1
		if self.i >= len(self.data):
			return False

		return self.data[self.i]

	def endData(self):
		return True if self.i >= len(self.data) - 1 else False

	def peek(self):
		return self.data[self.i]

	def push(self):
		self.istack.append(self.i)

	def pop(self):
		self.i = self.istack.pop()

	def iDec(self, n=1):
		self.i -= n


class OutputStream:
	def __init__(self, err):
		self.err = err

		self.data_list = []
		self.ln_list = []
		self.ln_no = 0
		self.i = -1

		self.global_label = None

	def newLine(self, n=1):
		self.data_list.append([])
		self.ln_no += n
		self.ln_list.append(self.ln_no)
		self.i += 1

	def delLine(self):
		res_d = []
		res_l = []
		for i in range(len(self.data_list)):
			if len(self.data_list[i]) != 0:
				res_d.append(self.data_list[i])
				res_l.append(self.ln_list[i])

		self.data_list = res_d
		self.ln_list = res_l

	def incLnNo(self):
		self.ln_no += 1

	def dataWriteInLine(self, word):
		self.data_list[self.i].append(word)

	def getLnNo(self):
		return self.ln_no

	def returnLists(self):
		return self.data_list, self.ln_list

	def setGlobalLabel(self, label_name):
		self.global_label = label_name

	def getGlobalLabel(self, label_name):
		if not (type(self.global_label) is None):
			return self.global_label

		self.err.addError(self.ln_no, "error", "Can't use local labels, when "
			                                     "don't established global label")
		return False # Switchs to ignore mode 


def __ws(s): # Checks white space
	while True:
		if s.getChar() is False:
			return False

		if s.peek() in " \t\r":
			continue

		if s.peek() == "\n":
				return True
	
		s.iDec()
		break

	return False

def __nl(s): # Checks new line char 
	while True:
		if s.getChar() != "\n":
			continue
		break

def __chekcNl(s):
	s.push()
	while True:
		if s.getChar() in string.whitespace:
			if s.peek() == "\n":
				return True

			continue

		break

	s.pop()
	return False

def __word(s, ctype, w_type=""): # Checks word (labels, instructions, arguments, etc...)
	res = ""
	while True:
		if s.getChar() in ctype:
			res += s.peek()

		#elif s.peek() == "@" and s.getChar() in "bf" and w_type == "called_label":
		#	return res + "@" + s.peek()

		else:
			s.iDec()
			return res

def _argCh(s): 
	if s.getChar() == ",":
		return True

	s.iDec()
	return False

def _commentCh(s):
	if s.getChar() == "#":
		return True

	s.iDec()
	return False

def _labelDeclaretion(s):
	if s.getChar() == ":":
		s.iDec()
		return True

	s.iDec()
	return False

def _nearestLabels(s):
	pass

def _stringCh(s):
	if s.getChar() == '"':
		print("AASA", s.peek())
		s.iDec()
		return True

	print(s.peek(), "aaaaaaa")
	s.iDec()
	return False

def _addressCh(s):
	if s.getChar() in "[]":
		return s.peek()

	s.iDec()
	return False

def _expressionCh(s):
	if s.getChar() in "()":
		return s.peek()

	s.iDec()
	return False



def grammar(err, data):
	s = Stream(err, data)
	outs = OutputStream(err)

	mode = 0
	# 0 - NORMAL MODE
	# 1 - STRING MODE
	# 2 - ADDRESSING MODE
	# 3 - EXPRESSION MODE
	# 4 - IGNORE MODE
	
	MAIN  = ( string.ascii_lowercase + 
		        string.ascii_uppercase +
		        string.digits )

	CTYPE  = ( MAIN +  "_.!:" )

	CTYPEA = ( MAIN + "_." )

	ATYPE  = ( CTYPEA + "+-*")

	ETYPE  = ( ATYPE + "/%~&|^")
 


	# ws*            CTYPE+ ws+ (arg ws* [, arg]*)? ws* nl+
	# ws* LABEL* ws+ CTYPE+ ws+ (arg ws* [, arg]*)? ws* nl+
	# ws* LABEL+ ws* nl+

	
	while True: # --> MAIN LOOP <--
		if s.endData():
			outs.delLine()
			return outs.returnLists()

		outs.newLine()
		ln_no = outs.getLnNo()

		if __ws(s):
			continue # if this line is empty, start parsing next line

		if _commentCh(s):
			__nl(s)
			continue # start parsing next line
		

		if _labelDeclaretion(s):
			outs.dataWriteInLine(__word(s, CTYPE)) # label declaration
			outs.newLine(0)
			if __ws(s):
				continue # start parsing next line 

		outs.dataWriteInLine(__word(s, CTYPE)) # instruction or dyrective

		if __ws(s):
			continue # start parsing next line

		if _commentCh(s):
			__nl(s)
			continue # start parsing next line

		while True: # arguments loop
			__ws(s)
			x = __word(s, CTYPEA)
			if x in ("byte", "half", "word"):
				outs.dataWriteInLine(x)
				if __ws(s):
					err.addError(ln_no, "error", f"After key word '{x}', must be argument")
					break

				__ws(s)
				outs.dataWriteInLine(__word(s, CTYPEA))

			if len(x) != 0:
				outs.dataWriteInLine(x)

			# argument type
			if _stringCh(s):
				outs.dataWriteInLine(__string(s, err, ln_no))

			elif _addressCh(s):
				outs.dataWriteInLine(__address(s, outs, err, CTYPEA))

			elif _expressionCh(s):
				outs.dataWriteInLine(__expression(s, outs, err, CTYPEA)) 

			if __ws(s):
				break # start parsing next line

			if _argCh(s):
				continue # next argument

			if _commentCh(s):
				__nl(s)
				break # start parsing next line

			if s.endData():
				return returnLists()
			err.addError(ln_no, "error", f"Bad syntax in place {s.peek()}")
	
			

def __string(s, err, ln_no):
	res = "" 
	string = False

	while True:
		x = s.getChar()
		if x == '"' and string == True:
			res += x
			break

		elif x == '"':
			string = True

		if x == "\n" or x == False:
			err.addError(ln_no, "error", "String must by ending")
			res = ""

		res += x

	return res

def __expression(s, outs, err, CTYPEA):
	res = ""
	l = 0
	char_list = "+*/&^%~|()$"
	word = True
	
	s.iDec()
	while True:
		x = s.getChar()
		ln_no = outs.getLnNo()
		
		if x == "\n":
			outs.incLnNo()
			continue 

		if x == "(":
			l += 1
			res += " ( "
			continue

		if x == ")":
			l -= 1
			res += " ) "
			if l == 0:
				return res
			continue

		if x == "#":
			err.addError(ln_no, "error", "Can't place '#' inside of the bracket")

		if x not in (char_list + " \t"):
			if x in "-~" and res[-1] not in " \t":
				err.addError(ln_no, "error", 
				              f"Mark {x} is unacceptable in middle of the word")
			
			res += x
			word = False
			continue

		if word == True and x in " \t":
			continue

		while True:
			if x in char_list:
				if word == True:
					err.addError(ln_no, "error", f"Bad syntax in place {x}")
					break

				res += f" {x} "
				word = True
				break

			if x not in " \t":
				err.addError(ln_no, "error", f"Bad syntax in place {x}")
				break

			x = s.getChar()

def __address(s, outs, err, CTYPEA):
	res = ""
	i = 0

	while True:
		x = s.getChar()
		ln_no = s.getLnNo()

		if x == "\n":
			err.addError(ln_no, "error", "Address must by ending")

		if x == "[" and i == 0:
			x = " [ "
			w = True
			continue

		elif x == "[":
			err.addError(ln_no, "error", f"Can't open address bracket in address")
			break

		if x == "]":
			res += " ] "
			break

		if x == "(" and w == True:
			s.iDec()
			res += __expression(s, outs, err, ln_no, CTYPEA)
			continue

		if x == "#":
			err.addError(ln_no, "error", "Can't place '#' inside of the bracket")

		if x in "+-*" and w == False:
			res += f" {x} "
			w = True
			continue

		elif x in "+-*":
			err.addError(ln_no, "error", f"Bad syntax in place {x}")
			break

		if x in CTYPEA:
			res += x
			w = False
			continue

	return res



