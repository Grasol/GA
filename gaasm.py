import os
import sys
import string

def comment(t,com):
	if t == "":
		com = True

	t = set(t)
	if '#' in t:
		com = True
	return com


def tag(t,ln_out,momentag):
	momentag.append(str(ln_out))
	momentag.append(t[1:])

	return momentag

def arginstr(idinstr,output,ni,countout,ln_no,t):
	syntax10 = ["mov","ld","str","add","sub","inc","dec","mul","div","imul","idiv","mod","or","and","xor","not","shl","shr","sal","sar","cmp"]
	syntax11 = ["jc","ja","jnc","jp","jnp","jad","jnad","jz","je","jnz","jne","js","jns","jae","jb","jbe","jmp","call"]
	syntax12 = ["put","get","prt","scan","crl","crs"] #SYNTAXY POMOCZNICZE

	if idinstr <= 2 and ni in syntax10:
		#output.append("")
		if t == "a":
			output[countout] += " 00"
		elif t == "b":
			output[countout] += " 01"
		elif t == "c":
			output[countout] += " 02"
		elif t == "d":
			output[countout] += " 03"
		elif t == "e":
			output[countout] += " 04"
		elif t == "h":
			output[countout] += " 05"
		elif t == "l":
			output[countout] += " 06"
		elif t == "sp":
			output[countout] += " 07"
		elif t == "pc":
			output[countout] += " 08"
		elif t == "ar":
			output[countout] += " 09"
		elif t == "ir":
			output[countout] += " 0A"
		else:
			ln_no += 1
			raise Exception("Syntax Error in line:",ln_no,t)

	elif idinstr == 1 and ni in syntax11:	
		output[countout] += " "
		output[countout] += t
	
	elif idinstr == 1 and ni == "push" or ni == "pop" or ni == "jmpr" or ni == "callr":
		#output.append("")
		if t == "a":
			output[countout] += " 00"
		elif t == "b":
			output[countout] += " 01"
		elif t == "c":
			output[countout] += " 02"
		elif t == "d":
			output[countout] += " 03"
		elif t == "e":
			output[countout] += " 04"
		elif t == "h":
			output[countout] += " 05"
		elif t == "l":
			output[countout] += " 06"
		elif t == "sp":
			output[countout] += " 07"
		elif t == "pc":
			output[countout] += " 08"
		elif t == "ar":
			output[countout] += " 09"
		elif t == "ir":
			output[countout] += " 0A"
		else:
			ln_no += 1
			raise Exception("Syntax Error in line:",ln_no,t)

	elif idinstr >= 2 and ni == "set":
		#output.append("")
		if idinstr == 1:
			if t == "a":
				output[countout] += " 00"
			elif t == "b":
				output[countout] += " 01"
			elif t == "c":
				output[countout] += " 02"
			elif t == "d":
				output[countout] += " 03"
			elif t == "e":
				output[countout] += " 04"
			elif t == "h":
				output[countout] += " 05"
			elif t == "l":
				output[countout] += " 06"
			elif t == "sp":
				output[countout] += " 07"
			elif t == "pc":
				output[countout] += " 08"
			elif t == "ar":
				output[countout] += " 09"
			elif t == "ir":
				output[countout] += " 0A"
			else:
				ln_no += 1
				raise Exception("Syntax Error in line:",ln_no,t)
		
		elif idinstr == 2 and ni == "set":
			#output.append("")
			try:
				t = int(t)
			except:
				ln_no += 1
				raise Exception("Syntax Error in line:",ln_no,t)
			immx = hex(t)
			immx = str(immx)
			output[countout] += " "
			output[countout] += immx[2:]

		
	return output

def instr(ni,output,ln_no):
	if ni == "mov":
		output.append("00")
	elif ni == "set":
		output.append("01")
	elif ni == "ld":
		output.append("02")
	elif ni == "str":
		output.append("03")
	elif ni == "add":
		output.append("10")
	elif ni == "sub": 
		output.append("11")
	elif ni == "inc":
		output.append("12")
	elif ni == "dec":
		output.append("13")
	elif ni == "mul":
		output.append("14")
	elif ni == "div" or ni == "idiv":
		output.append("15")
	elif ni == "imul":
		output.append("16")
	elif ni == "mod":
		output.append("17")
	elif ni == "or":
		output.append("18")
	elif ni == "and":
		output.append("19")
	elif ni == "xor":
		output.append("1A")
	elif ni == "not":
		output.append("1B")
	elif ni == "shl" or ni == "sal":
		output.append("1C")
	elif ni == "shr":
		output.append("1D")
	elif ni == "sar":
		output.append("1E")
	elif ni == "cmp":
		output.append("20")
	elif ni == "jc" or ni == "jae":
		output.append("21")
	elif ni == "jnc":
		output.append("22")
	elif ni == "jp":
		output.append("23")
	elif ni == "jnp":
		output.append("24")
	elif ni == "jad":
		output.append("25")
	elif ni == "jnad":
		output.append("26")
	elif ni == "jz" or ni == "je":
		output.append("27")
	elif ni == "jnz" or ni == "jne":
		output.append("28")
	elif ni == "js":
		output.append("29")
	elif ni == "jns":
		output.append("2A")
	elif ni == "ja":
		output.append("2B")
	elif ni == "jb":
		output.append("2C")
	elif ni == "jbe":
		output.append("2D")
	elif ni == "push":
		output.append("30")
	elif ni == "pop":
		output.append("31")
	elif ni == "jmp":
		output.append("40")
	elif ni == "jmpr":
		output.append("41")
	elif ni == "call":
		output.append("42")
	elif ni == "callr":
		output.append("43")
	elif ni == "ret":
		output.append("44")
	elif ni == "put":
		output.append("F0")
	elif ni == "get":
		output.append("F1")
	elif ni == "prt":
		output.append("F2")
	elif ni == "scan":
		output.append("F3")
	elif ni == "intr":
		output.append("F4")
	elif ni == "crl":
		output.append("F5")
	elif ni == "crs":
		output.append("F6")
	elif ni == "exit":
		output.append("FF")
	else:
		ln_no += 1
		raise Exception("Syntax Error in line:",ln_no,t)

	return output


def parser(t,ln_no,oneline,i,idinstr,output,ni,countout,comment,syntax0):
	ctype = set("_.!:#")
 
	#t = set(t)
	#problem = t & ctype

	#elif '#' in problem:
	#	comment = True
	#	print("comment",comment)
	#	return output #TODO: DO NASTĘPNEJ LINIKI 

	t = token(i,oneline,t)
	#CTYPE1 = string.ascii_letters + string.digits
	if t == []:
		pass
	elif t in syntax0:
		ni = t #nameinstruction = ni
		oneline = instr(ni,output,ln_no)
	elif idinstr != 0:	
		oneline = arginstr(idinstr,output,ni,countout,ln_no,t)

	else:
		ln_no += 1
		raise Exception("Syntax Error in line:",ln_no,t) #JEŻELI NIC SIĘ NIE UDAŁO: SYNTAX ERROR

	return output

def token(i,oneline,t):
	i
	t = oneline[i]
	return t

def ln(countout,data,ln_no):
	countout += 1 #NALICZA LINIJKI W KOMPILACJI
	try:
		oneline = data[ln_no]
	except:
		online = ""
		return online
	oneline = oneline.split()
	return oneline

def main():
	syntax0 = ["mov","set","ld","str","add","sub","inc","dec","mul","div","imul","idiv","mod","or","and","xor","not","shl","shr","sal","sar","cmp","jc","ja","jnc","jp","jnp","jad","jnad","jz","je","jnz","jne","js","jns","jae","jb","jbe","push","pop","jmp","jmpr","call","callr","ret","exit","intr","put","get","prt","scan","crl","crs"]
	syntax11 = ["jc","ja","jnc","jp","jnp","jad","jnad","jz","je","jnz","jne","js","jns","jae","jb","jbe","jmp","call"]
	i = -1 #KOLUMNA LINIJKI
	t = None #TOKEN
	ln_no = -1 #NUMER LINIJKI
	idinstr = -1
	ln_out = 0
	countout = -1
	com = False
	name_tag = []
	jump_tag = []
	output = []
	ni = ""
	momentag = []
	listag = []
	appointment = 0 #0 Brak dodatkowego tokena
					#1 Tylko jeden token (możliwe wszystko)
					#2 Tylko jeden token (tylko rejestr)
					#3 Tylko jeden token (tylko int)
					#4 Tylko jeden token (tylko str)
					#5 Tylko jeden token (int str)
					#6
	if len(sys.argv) != 2 :
		sys.exit("Name_File Error. Must be: gaasm.py [name_file.txt]") #JAK PODANO ZŁE INFO, WYWALA NA STARCIE
	if sys.argv[1] == "/?":
		sys.exit("Compiler Grasol Architecture Asembler (ccarchasm) v0.1 . Grasol 2019")

	infilename = sys.argv[1]
	with open(infilename) as f:
		data = f.read().splitlines() #PODZIEL KOD NA CZĘŚCI
		ln_start = len(data)

	#WYDZIEL JEDNĄ LINIKE KODU: KOD Z LINIJKI / NUMER LINII
	#JEDNO SŁOWO Z LINIJKI PRZEZ KOLUMNE i
	#PARSER
	#PRZEZ PARSER DO OUT LUB NIC
	#OD POCZĄTKU AŻ SIĘ LINIJKI NIE SKOŃCZĄ
	while ln_no != ln_start:
		com = False
		ln_no += 1
		countout += 1
		i = 0
		idinstr = -1 #NALICZA ARGUMENTY
		oneline = ln(countout,data,ln_no) # P A M I Ę T A J   O   ln_out! MA BYĆ NALICZANE ZA KAŻDE ni I :etykiety!!!! ALE PÓŹNIEJ PO TAG ln_out -= 1
		i_start = len(oneline)
		
		if oneline == []:
			print("print oneline",oneline)
			countout -= 1
			#ln_out -= 1
		
		while i_start != i:
			idinstr +=1
			ni = oneline[0]
			t = token(i,oneline,t)
			com = comment(t,com)
			print(ln_out,ni,i)
			if ni in syntax0 and i == 0:
				ln_out += 1	
			
			if ':' in t[0]:
				ln_out += 1
				momentag = tag(t,ln_out,momentag)
				com = True
				ln_out -= 1
			
			if com == False:
				output = parser(t,ln_no,oneline,i,idinstr,output,ni,countout,comment,syntax0)
				i += 1
			
			elif com == True:
				i = i_start
				countout -= 1
			
			if ni in syntax11 and i > 1:
					listag.append(t)

	phase2control = True
	xmoment = -1
			
	# P H A S E 2 !!!!!!! momentag co dwa == jakiś element z output! zastąpić jakiś element na ln_out! KAŻDĄ ETYKIETE W JUMPIE PODAWAĆ DO LISTAG. JEŻELI output[coś tam] == momentag USUŃ Z LISTAG!!!! JEŚLI COŚ W NIEJ ZOSTANIE E X C E P T I O N!!!!!!!!
	while phase2control == True:
		xmoment += 2
		outputlistc = -1
		finishwhile = 0
		print("output",output,"momentag",momentag,"listag",listag,"xmoment",xmoment)
		try:
			for outelement in output:
				outputlistc += 1
				if momentag[xmoment] in outelement:
					outelement = outelement.split()
					outelement[1] = momentag[xmoment - 1]
					if momentag[xmoment] in listag:
						output[outputlistc] = ' '.join(outelement)
						while len(listag) > finishwhile:
							if listag[finishwhile] == momentag[xmoment]:
								del listag[finishwhile]
							finishwhile += 1

		except:
			print(listag,"listag")
			if listag != []:
				for listagelement in listag:
					print("Does not know where to jump",listagelement)
				raise Exception("Tag Error/s")
			phase2control = False
	
	f.close()
	print(momentag)
	outfilename = infilename + ".hex"
	with open(outfilename,"w") as f:
		for element in output:
			element += "\n"
			f.write(element)
	f.close()

	print("good job!")

if __name__ == "__main__":
	main()