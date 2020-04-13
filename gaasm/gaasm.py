from grammar import grammar
import sys
import os

class GAASMException(Exception):
	def __init__(self, f_name):
		self.f_name = f_name
		self.errors = []
		self.store_result = True
		# if throwed at least one error (no warning), gaasm will not store bytecode
		# resultat
	
	def fatalError(self, context):
		raise GAASMException(f"{self.f_name}:fatal error: {context}")
	
	def addError(self, ln_no, type_error, context):
		self.errors.append(f"{self.f_name}:{ln_no}:{type_error}: {context}")
		if type_error == "error":
			self.store_result = False

	def printError(self):
		if self.store_result:
			return True

		for err in self.errors:
			sys.stderr.write(f"{err}\n")

		return False


class Assembler:
	def __init__(self, in_f_name):
		self.grm = grammar
		self.err = GAASMException(in_f_name)

		self.output = []

	def phase1(self):
		return self.grm(self.err, self.data)

	def run(self, data):
		self.data = data
		ln, ind = self.phase1()
		for i in range(len(ind)):
			print(ind[i], ln[i])
		

		#self.phase2()
		if self.err.printError():
			#return self.phase3()
			pass


def main():
	if len(sys.argv) != 2:
		sys.exit("usege: gaasm.py <file_name.asm>")

	in_f_name = sys.argv[1]
	#out_f_name = os.path.splittext(in_f_name)[0] + ".bin"

	with open(in_f_name, "r") as f:
		data = f.read()

	asm = Assembler(in_f_name)
	bytecode = asm.run(data)
	if type(bytecode) is None:
		sys.exit(1)

	#with open(out_f_name, "wb") as f:
	#	f.write(bytecode)

if __name__ == "__main__":
	main()