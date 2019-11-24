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

def lenn(lst):
	x = 0
	for l in lst:
		if l != None:
			x += 1
	return x

	
class OutputParsing():
	def __init__(self):
		self.byte = bytearray(0)
		self.err = []

	def reset(self, ln ,n):
		self.ln = ln
		self.n = n 
		self.opcode = opcode_return()
		self.reg8 = {"ra":0x0,"rd":0x1,"re":0x2,"rc":0x3,"rb":0x4,"sp":0x5,"rx":0x6,"ry":0x7,"rah":0x0,"rdh":0x1,"reh":0x2,"rch":0x3,"rbh":0x4,"sph":0x5,"rxh":0x6,"ryh":0x7}
		self.reg8n = {"ra":0x0,"rd":0x1,"re":0x2,"rc":0x3,"rb":0x4,"sp":0x5,"rx":0x6,"ry":0x7}
		self.reg8hh = {"rah":0x0,"rdh":0x1,"reh":0x2,"rch":0x3,"rbh":0x4,"sph":0x5,"rxh":0x6,"ryh":0x7}
		self.reg8h = {"rah":0x0,"rdh":0x1,"reh":0x2,"rch":0x3}
		self.reg16 = {"wra":0x0,"wrd":0x1,"wre":0x2,"wrc":0x3,"wrc":0x4,"wsp":0x5,"wrx":0x6,"wry":0x7}
		self.a = [None,None,None]
		self.pa = 0
		self.chkt = 0
		self.mnec = None
		self.tupple = None
		self.imm = None
		self.rmode = None

	def put_tokens(self, d):
		nt = 0
		for token in d:
			nt += 1
			if self.mnec == None:
				self.mnec = token
				continue
			if token == ",":
				if nt == 3 or nt == 5:
					self.pa += 1
					continue
				self.err.append("Error in line %i: Syntax"%(self.ln[self.n]))
				return True

			if nt == 2 or nt == 4 or nt == 6: 	
				self.a[self.pa] = (token)
				continue
			self.err.append("Error in line %i: Syntax"%(self.ln[self.n]))
			return True
		
		return False

	def check_instruction(self):
		if self.mnec in self.opcode:
			self.tupple = self.opcode[self.mnec]
			return False

		self.err.append("Error in line %i: %s: bad instruction"%(self.ln[self.n],self.mnec))
		return True

	def check_arguments(self):
		#self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],self.a[0]))
		narg = 0	
		self.rmode = None	
		self.type = "8"		
		if self.tupple[1] == 0: # 0 ARGUMENTS
			for at in self.a:

				if at == None:
					continue
				else:
					self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))
					break

		elif self.tupple[1] == 1 or self.tupple[1] == 8: # 1 ARGUMENTS
			for at in self.a:

				if narg == 0 and self.tupple[1] == 1: 
					narg += 1
					if at in self.reg8:
						if at in self.reg8hh:
							self.rmode = "Mnh"
						else:
							self.rmode = "Mn"
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))
						break

				elif narg == 0 and self.tupple == 8:
					narg += 1
					if tohex(at) != "error":
						self.a[0] == tohex(at)
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))

				elif narg != 0:
					if at == None:
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))
						break
		
		elif self.tupple[1] == 2 or self.tupple[1] == 3: # 2 or 3 ARGUMENTS
			for at in self.a:
				print(at, narg)
				if narg == 0:
					narg += 1
					if at in self.reg8:
						if at in self.reg8h:
							self.rmode = "H"
							continue
						if at in self.reg8hh:
							self.rmode = "HH"
							continue
						if at in self.reg8n:
							if at in ["ra","rd","re","rc"]:
								self.rmode = "n"
							else:
								self.rmode = "N"
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))

				elif narg == 1:
					narg += 1
					if at in self.reg8:
						if self.rmode == "H":
							if at in self.reg8n:
								continue
							if at in self.reg8hh:
								self.rmode = "HH"
								continue
						if self.rmode == "HH":
							if at not in self.reg8hh:
								self.err.append("Error in line %i: You can't usege this register: %s"%(self.ln[self.n],at))
								break
							continue
						if self.rmode == "N" or self.rmode == "n":
							if at in self.reg8n:
								self.rmode = "N"
								continue
							if at in self.reg8hh:
								if self.rmode == "n":
									self.rmode = "H"
									continue
								else:
									self.err.append("Error in line %i: You can't usege this register: %s"%(self.ln[self.n],at))
									break

					elif tohex(at) != "error":
						self.a[1] = tohex(at)
						if self.a[1] >= 256:
							self.err.append("Error in line %i: Number %i is to big"%(self.ln[self.n],self.a[1]))
							break
						if self.rmode == "H":
							self.rmode = "Mih"
						else:
							self.rmode = "Mi"
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))
						break

				elif narg == 2 and self.tupple[1] == 2:
					if at == None:
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))
						break

				elif narg == 2 and self.tupple[1] == 3:
					if tohex(at) != "error":
						self.imm = tohex(at)
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))
						break

		elif self.tupple[1] == 22: # 2 WORD ARGUMENTS 
			self.type = "16"
			for at in self.a:
				if narg == 0:
					narg += 1
					if at in self.reg16:
						self.rmode = "N"
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))

				if narg == 1:
					narg += 1
					if at in self.reg16:
						continue
					elif tohex(at) != "error":
						self.a[1] = tohex(at)
						if self.a[1] >= 65536:
							self.err.append("Error in line %i: Number %i is to big"%(self.ln[self.n],self.a[1]))
							break
						self.rmode = "Mi"
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))
						break

				elif narg == 2:
					if at == None:
						continue
					else:
						self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],at))
						break

		elif self.tupple[1] == 4 or self.tupple[1] == 5:
			pass

		elif self.tupple[1] == 9:
			pass


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

	def dyrectives(self, asmline):
		if asmline[0][0:2] == "db":
			del asmline[0]
			print(asmline,"ASASAS")
			asmline = ' '.join(asmline)
			asmline = asmline.split(",")
			print(asmline,"ASMLINE")
			for token in asmline:
				if token[0] == '"' and token[-2] == '"':
					token = token[1:-1]
					print("TOKENTOKEN",token)
					self.byte.extend(map(ord, token))
					continue

				if tohex(token) == "error":
					self.err.append("Error in line %i: Syntax: %s"%(self.ln[self.n],token))
					break
				self.byte.append(tohex(token))
			return True
		return False
				



	def get_out(self):
		print("--->",self.byte)
		return (self.err, self.byte)

	def q_err(self):
		if len(self.err) == 0:
			return True
		return False








	

def parsing_control(data, ln):
	n = -1
	outp = OutputParsing()
	for d in data:
		n += 1
		outp.reset(ln,n)
		d = d.split()
		if outp.dyrectives(d):
			continue

		if outp.put_tokens(d):
			continue

		if outp.check_instruction():
			continue

		if outp.check_arguments():
			continue

		if outp.q_err():
			outp.byte_out()


	try:
		return outp.get_out()
	except:
		return
 

				












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

