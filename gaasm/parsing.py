#mov ra, rb   mov [00][000][001]
#ld ra, [rb]  ld [00][000][001]
#mov ra, 0x20 mov [01][000][001] [0010 1000]
#mov ra, 32   mov [01][000][001] [0000 0100]
#st [ra+14], rc st [00][000][010] [1110 0000 0000 0000] 
#st [ra+14], 14 st [01][000][001] [1110 0000 0000 0000] [1110 0000]
#add rd, re   add [00][011][100]
#
#
#[xx][xxx][xxx]
#00-normal 01-mode 10-reserved 11-reserved 
from enum import Enum

def tohex(n):
	try:
		if n[-1:] == "h":
			n = n[:-1]
			n = int(n,16)
		elif n[-1:] == "b":
			n = n[:-1]
			n = int(n, 2)
		else:
			n = int(n)
	except:
		n = "error"

	return n

def pindex():
	pass
	

class TokenType(Enum):
	LABEL = 0
	LABEL_CHAR = 1
	IDENTIFIER = 2
	EXPRESSION = 3
	DYRECTIVE = 4
	REGISTER_8 = 5
	REGISTER_16 = 6
	REGISTER_8h = 7
	IMMEDIATE_VALUE = 8
	IMMEDIATE_VALUE2 = 9
	REG_ADDRESS = 10
	DISP_ADDRESS = 11
	DISP2_ADDRESS = 12
	DOUBLE_REG_ADDRESS = 13
	DOUBLE_DISP_ADDRESS = 14
	DOUBLE_DISP2_ADDRESS = 15
	LITERAL_STRING = 16
	LITERAL_HEX = 17


class Tokens_Parser():
	def __init__(self):
		self.opcode = opcode_return()
		self.reg8 = {"ra":0x0,"rd":0x1,"re":0x2,"rc":0x3,"rb":0x4,"sp":0x5,"rx":0x6,"ry":0x7}
		self.reg8h = {"rah":0x0,"rdh":0x1,"reh":0x2,"rch":0x3,"rbh":0x4,"sph":0x5,"rxh":0x6,"ryh":0x7}
		self.reg16 = {"wra":0x0,"wrd":0x1,"wre":0x2,"wrc":0x3,"wrc":0x4,"wsp":0x5,"wrx":0x6,"wry":0x7}
		self.ltokens = []

	def start_parsing(self, lines):
		i = 0
		for line in lines:
			if self.first_element(line[0]):
				pass #ERR

			self.second_element(line[1:], i)
			i += 1

		return self.ltokens

	def first_element(self, t):
		if t in self.opcode:
			self.ltokens.append([TokenType.IDENTIFIER, t])
			return False

		if t[0] == ":" or t[0] == ".":
			self.ltokens.append([TokenType.LABEL_CHAR, t])
			self.ltokens.append([TokenType.LABEL, t[1:]])
			return False

		if t[0] == "!":
			if t[1:] == "org":
				self.ltokens.append([TokenType.DYRECTIVE, t[1:]])
				return False
			else:
				pass #ERR

		if t in ["db","dw","dd","dq"]:
			self.ltokens.append([TokenType.DYRECTIVE, t])
			return False

		#ERR
		print(t)

	def second_element(self, elements, i):
		for t in elements:
			if t in self.reg8:
				self.ltokens[i] += (TokenType.REGISTER_8, t)

			elif t in self.reg8h:
				self.ltokens[i] += (TokenType.REGISTER_8h, t)

			elif t in self.reg16:
				self.ltokens[i] += (TokenType.REGISTER_16, t)

			elif tohex(t) != "error":
				self.ltokens[i] += (TokenType.IMMEDIATE_VALUE, tohex(t))

			elif t[0] == "[" and t[-1] == "]":
				address_argument(t, i)

			elif t[0] == '"' and t[-1] == '"':
				self.ltokens[i] += (TokenType.LITERAL_STRING, t[1:-1])

			else:
				self.ltokens[i] += (TokenType.EXPRESSION, t)

	def address_argument(self, t, i):
		addr = 0
		if t[0:1] == "[[" and t[-2:-1] == "]]":
			t = t[2:-2]
			addr = 2

		elif t[0] == "[" and t[-1] == "]":
			t = t[1:-1]
			addr = 1

		templ = []
		string = ""
		for char in t:
			if char == "+":		
				templ.append(self.address_element(string))
				continue
			string += char

		REGISTER = []
		DISP = []
		LABEL = []
		expr = False
		for t in templ:
			if t[0] == TokenType.REGISTER_16 or t[0] == TokenType.REGISTER_8 or t[0] == TokenType.REGISTER_8h:
				REGISTER.append(t)

			elif t[0] == TokenType.LITERAL_HEX:
				if tohex(t[1]) < 256:
					t[1] = tohex(t[1])
					t[0] = TokenType.IMMEDIATE_VALUE
				elif tohex(t[1]) < 2**16:
					t[1] = tohex(t[1])
					t[0] = TokenType.IMMEDIATE_VALUE2

				DISP.append(t)

			elif t[0] == TokenType.LABEL:
				LABEL.append(t)

		if len(REGISTER) > 1:
			#TODO err
			pass

		if len(DISP) > 1 and len(LABEL) > 0: 
			expr = True

		if len(REGISTER) == 1 and len(DISP) == 0 and len(LABEL) == 0:
			if addr == 1:
				self.ltokens[i].append(TokenType.REG_ADDRESS)
			elif addr == 2:
				self.ltokens[i].append(TokenType.DOUBLE_REG_ADDRESS)
			self.ltokens[i] += REGISTER[0]

		elif len(DISP) == 1 and len(LABEL) == 0:
			if DISP[0][0] == TokenType.IMMEDIATE_VALUE:
				if addr == 1:
					self.ltokens[i].append(TokenType.DISP_ADDRESS)
				elif addr == 2:
					self.ltokens[i].append(TokenType.DOUBLE_DISP_ADDRESS)
			
			elif DISP[0][0] == TokenType.IMMEDIATE_VALUE2:
				if addr == 1:
					self.ltokens[i].append(TokenType.DISP2_ADDRESS)
				elif addr == 2:
					self.ltokens[i].append(TokenType.DOUBLE_DISP2_ADDRESS)

			if len(REGISTER) == 1:
				self.ltokens[i] += REGISTER[0]
			self.ltokens[i] += DISP[0]

		else:
			if addr == 1:
				self.ltokens[i].append(TokenType.DISP2_ADDRESS)
			elif addr == 2:
				self.ltokens[i].append(TokenType.DOUBLE_DISP2_ADDRESS)

			if len(REGISTER) == 1:
				self.ltokens[i] += REGISTER[0]
			self.ltokens[i].append(TokenType.EXPRESSION)
			for d in DISP:
				self.ltokens[i] += d
			for l in LABEL:
				self.ltokens[i] += l

	def address_element(self, string):
		if string in self.reg8:
			return [TokenType.REGISTER_8, string]

		if string in self.reg8h:
			return [TokenType.REGISTER_8h, string]

		if string in self.reg16:
			return [TokenType.REGISTER_16, string]

		if tohex(string) != "error":
			return [TokenType.LITERAL_HEX, tokex(string)]

		return [TokenType.LABEL, string]

	def count_label(self):
		pass


















class ByteOutput():
	

	def byte_out(self):
		print(self.rmode)
		imm2 = None
		self.byte.append(self.tupple[0])
		if self.type == "8":
			if self.rmode == "N":
				self.rmode = 0
				r1 = self.reg8n[self.a[0]]
				r2 = self.reg8n[self.a[1]]
	
			if self.rmode == "Mn":
				self.rmode = 1
				print(self.tupple[0] ,self.a)
				r1 = self.reg8n[self.a[0]]
				r2 = 0
	
			if self.rmode == "Mi":
				self.rmode = 1
				r1 = self.reg8n[self.a[0]]
				r2 = 1
				self.imm = self.a[1]
	
			if self.rmode == "Mnh":
				self.rmode = 1
				r1 = self.reg8hh[self.a[0]]
				r2 = 4
	
			if self.rmode == "Mih":
				self.rmode = 1
				r1 = self.reg8hh[self.a[0]]
				r2 = 5
				self.imm = self.a[1]
	
			if self.rmode == "H":
				self.rmode = 2
				r1 = self.reg8[self.a[0]]
				r2 = self.reg8[self.a[1]]
	
			if self.rmode == "HH":
				self.rmode = 3
				r1 = self.reg8hh[self.a[0]]
				r2 = self.reg8hh[self.a[1]]

		if self.type == "16":
			if self.rmode == "N":
				self.rmode = 0
				r1 = self.reg16[self.a[0]]
				r2 = self.reg16[self.a[1]]

			if self.rmode == "Mi":
				self.rmode = 1
				r1 = self.reg16[self.a[0]]
				r2 = 1
				self.a[1] = hex(self.a[1]) + "00"
				self.imm = self.a[1][2:4]
				imm2 = self.a[1][4:6]

		print(self.rmode,r1,r2)
		print(self.imm,imm2)
		self.byte.append(self.rmode<<6 | r1<<3 | r2)
		if self.imm != None:
			self.byte.append(self.imm)
		if imm2 != None: 
			self.byte.append(imm2)

		print("->",self.byte)

	

	def get_out(self):
		print("--->",self.byte)
		return (self.err, self.byte)

	def q_err(self):
		if len(self.err) == 0:
			return True
		return False








	

def parsing_control(data, ln):
	pass
 

				












def opcode_return():
	# 0 - brak argumentów
	# 1 - M nope
	# 2 - N/M/H
	# 3 - N/M/H + imm
	# 4 - adres
	# 5 - adres + disp
	# 8 - imm
	# 9 - label 
	# 22 - word N

	instrOpcode = {"mov" :(0x00, 2,0x02, 22),#a = b
                 "lea" :(0x01, 2),#reg = address
                 "ldr" :(0x03, 4),#[reg]
                 "str" :(0x04, 4),#[reg]
                 "ld":(0x05, 5, 0x07, 5),#[reg+disp1/2]
                 "st":(0x06, 5, 0x08, 5),#[reg+disp1/2]
                 "xchg":(0x09, 2), #a = b, b = a
                 "crl" :(0x0A, 2), #load control reg
                 "crs" :(0x0B, 2), #store control reg
                 "bcw" :(0x0C, 1), #byte reg conver word reg

                 "add" :(0x10, 2),#a += b 
                 "sub" :(0x11, 2),#a -= b 
                 "inc" :(0x12, 1),#a++
                 "dec" :(0x13, 1),#a--
                 "mul": (0x14, 2),#WAH = a * b
                 "div": (0x15, 2),#WAH = a / b
                 "muls":(0x16, 1, 0x2B, 2),#WAH = a * A, WAH = a * b signed mul
                 "divs":(0x17, 2),#WAH = a / b signed div
                 "or"  :(0x18, 2),#a |= b
                 "and" :(0x19, 2),#a &= b
                 "xor" :(0x1A, 2),#a ^= b
                 "not" :(0x1B, 1),#~a
                 "neg" :(0x1C, 1),#~a++
                 "shl" :(0x1D, 2),#a<< 
                 "shr" :(0x1E, 2),#a>> 
                 "sal" :(0x1D, 2),#a<< 
                 "sar" :(0x1F, 2),#+-a>> 
                 "cmp" :(0x20, 2),#a-b
                 "test":(0x21, 2),#a && b
                 "rol" :(0x22, 2),#rotation left 
                 "ror" :(0x23, 2),#rotation right 
                 "adc" :(0x24, 2),#add with carry
                 "sbb" :(0x25, 2),#add witch borrow
                 "rcr" :(0x26, 2),
                 "rcl" :(0x27, 2),
                 "addi":(0x28, 3),# a = b + imm
                 "subi":(0x29, 3),# a = b - imm

                 "push":(0x30, 1),#a -> top stack
                 "pop" :(0x31, 1),#a = top stack

                 "bt"  :(0x40, 2),#bit test
                 "btc" :(0x41, 2),#bit test and complement 
                 "bts" :(0x42, 2),#bit test set
                 "btr" :(0x43, 2),#bit test reset
                 "bsf" :(0x44, 2),#bit scan forward
                 "bsr" :(0x45, 2),#bit scan revers 
                 "lebg":(0x46, 1),#swap little endian <-> big endian
                 "scf" :(0x47, 0),#set carry flag
                 "rcf" :(0x48, 0),#reset carry flag
                 "lrf" :(0x49, 1),#load rf
                 "srf" :(0x4A, 1),#store rf

                 "jc"  :(0x51, 9),#jump if carry flag == 1
                 "jnc" :(0x52, 9),#jump if carry flag == 0
                 "jz"  :(0x53, 9),#jump if zero flag == 1
                 "jnz" :(0x54, 9),#jump if zero flag == 0
                 "jp"  :(0x55, 9),#jump if parity flag == 1
                 "jnp" :(0x56, 9),#jump if parity flag == 0
                 "jac" :(0x57, 9),#jump if adjust flag (auxiliary carry flag) == 1
                 "jnac":(0x58, 9),#jump if adjust flag (auxiliary carry flag) == 0 
                 "jo"  :(0x59, 9),#jump if overflow flag == 1
                 "jno" :(0x5A, 9),#jump if overflow flag == 0
                 "js"  :(0x5B, 9),#jump if sign flag == 1
                 "jns" :(0x5C, 9),#jump if sign flag == 0
                 "ja"  :(0x5E, 9),#jump if above (CF == 1 and ZF == 0)
                 "jae" :(0x52, 9),#jump if above or equal (CF == 0)
                 "je"  :(0x53, 9),#jump if equal (ZF == 1)
                 "jne" :(0x54, 9),#jump if not equal (ZF == 0)
                 "jb"  :(0x51, 9),#jump if bellow (CF == 1)
                 "jbe" :(0x59, 9),#jump if bellow or equal (CF == 1 or ZF == 1)
                 "jg"  :(0x60, 9),#jump if greater (ZF == 0 and SF == OF)
                 "jge" :(0x61, 9),#jump if greater or equal (SF == OF)
                 "jl"  :(0x62, 9),#jump if less (SF != OF)
                 "jle" :(0x63, 9),#jump if less or equal (ZF == 1 SF != OF)
                 "jmp" :(0x64, 9),#jump
                 "call":(0x65, 9,),#call
                 "ret" :(0x66, 0),#return
                 "loop":(0x67, 9),#loop
                 "callr":(0x68,1),
                 "jmpr":(0x69, 1),

                 "wait":(0x80, 0),#wait						    
                 "int" :(0x81, 8),#interrupt
                 "intr" :(0x82, 1),#interrupt (reg)
                 "iret":(0x83, 0),#interrupt return 
                 "halt" :(0x84, 0),#halt
                 "nop" :(0x86, 0),#nothing 
                 "cpuid":(0x8C,0),#CPU ID
                 "in"  :(0x90, 2),#in port
                 "out" :(0x91, 2),#out port

                 "end":(0xFF, 0)} #end program (interrupt)

	return instrOpcode

