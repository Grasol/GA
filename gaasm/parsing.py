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



class OutputParsing():
	def __init__(self, ln):
		self.output = bytearray(0)
		self.ln = ln
		self.opcode = opcode_return()
		self.reg8 = ["ra","rb","rc","rd","re","sp","rx","ry","sph","rxh","ryh"]
		self.reg8h = ["sph","rxh","ryh"]
		self.reg16 = ["wsp","wrx","wry"]

		self.A = None
		self.B = None
		self.C = None
		self.imm = None
		self.disp = None

	def instruction_token(self, mnec, n):
		self.mnec = mnec
		if self.mnec in self.opcode:
			self.insttuple = self.opcode[self.mnec]
			return 0
		print("Error in line %i: bad instruction: %s" % (self.ln[n], self.mnec))
		return 10


	def operand_tokens(self, tokens, n):
		if self.insttuple[1] == 0:
			return False

		if self.insttuple[1] == 1:
			self.A = tokens.pop()
			if self.mnec != tokens.pop():
				print("Error in line %i: bad syntax" % self.ln[n])
				return True
			return False

		if self.insttuple[1] == 2:
			self.A = tokens.pop()
			if "," == tokens.pop():
				self.B = tokens.pop()
				if self.mnec != tokens.pop():
					print("Error in line %i: bad syntax" % self.ln[n])
					return True
				return False

		if self.insttuple[1] == 3:
			pass
		return False
	

	def address_token(self):
		pass

	def argumet_byte(self):
		if self.A not in self.reg8:
			return True
			if self.B not in self.reg8:
				return True

		print("hello world")
		



	def imm_token(self):
		pass
	

def parsing_control(data, ln):
	n = -1
	for d in data:
		n += 1
		outp = OutputParsing(ln)
		tokennum = 0

		d = d.split()
		argmode = outp.instruction_token(d[0],n)
		if argmode == 10:
			continue
		

		d.reverse()
		mnec = d.pop()
		d.insert(0, mnec)
		if outp.operand_tokens(d,n):
			continue
		outp.argumet_byte()

 

				












def opcode_return():
	# mnemonik | opcode | (0-brak argumentów) (1-1 argument oper) (2-2 argumenty oper) (3-3 argumeny oper+imm)(4-adres)(5-adres+disp)(8-imm)(9-label)
	# reg: ra-0, rd-1, rb-2, rc-3, re-4, sp-5, rx-6, ry-7

	instrOpcode = {"mov" :(0x00, 2),#a = b
                 "lea" :(0x01, 2),#reg = address
                 "ldr" :(0x03, 4),#[reg]
                 "str" :(0x04, 4),#[reg]
                 "ld":(0x05, 5, 0x07, 5),#[reg+disp1/2]
                 "st":(0x06, 5, 0x08, 5),#[reg+disp1/2]
                 "xchg":(0x09, 2), #a = b, b = a
                 "crl" :(0x0A, 2), #load control reg
                 "crs" :(0x0B, 2), #store control reg

                 "add" :(0x10, 2),#a += b 
                 "sub" :(0x11, 2),#a -= b 
                 "inc" :(0x12, 1),#a++
                 "dec" :(0x13, 1),#a--
                 "mul" :(0x14, 1),#A:D = a * A 
                 "div" :(0x15, 1),#A:D = a / A 
                 "imul":(0x16, 1,0x22, 2,0x23, 3),#A:D = a * A, a *= b, a = b * imm
                 "idiv":(0x17, 2),#A:D = a / b
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
                 "rol" :(0x24, 2),#rotation left 
                 "ror" :(0x25, 2),#rotation right 
                 "adc" :(0x26, 2),#add with carry
                 "sbb" :(0x27, 2),#add witch borrow
                 "rcr" :(0x28, 2),
                 "rcl" :(0x29, 2),

                 "push":(0x30, 1),#a -> top stack
                 "pop" :(0x31, 1),#a = top stack

                 "bt"  :(0x40, 2),#bit test
                 "btc" :(0x41, 2),#bit test and complement 
                 "bts" :(0x42, 2),#bit test set
                 "btr" :(0x43, 2),#bit test reset
                 "bsf" :(0x44, 2),#bit scan forward
                 "bsr" :(0x45, 2),#bit scan revers 
                 "lebg":(0x46,1),#swap little endian <-> big endian
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
                 "jmpr":(0x69, 1),
                 "call":(0x65, 9),#call
                 "callr":(0x68,1),
                 "ret" :(0x66, 0),#return
                 "loop":(0x67, 9),#loop

                 "wait":(0x80, 0),#wait						    
                 "int" :(0x81, 8),#interrupt
                 "intr" :(0x82, 1),#interrupt (reg)
                 "iret":(0x83, 0),#interrupt return 
                 "hlt" :(0x84, 0),#halt
                 "nop" :(0x86, 0),#nothing 
                 "cpuid":(0x8C,0),#CPU ID
                 "in"  :(0x8E, 2),#in port
                 "out" :(0x8F, 2),#out port

                 "end":(0xFF, 0)} #end program (interrupt)

	return instrOpcode

