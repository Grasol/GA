# Copyright 2019 Grasol
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# opcode | r dst | r src | imm8 ; imm16
#dunder

import os
import sys
#import string
#import struct 
from syntax import *
from parsing import *
#import modgrammar



class Assembler():
	def __init__(self, data):
		self.data = data
		self.output = bytearray(0)
		self.synx = Syntax(data)

	def errasm(self,errs):
		self.errs.append(errs)

	def phase1(self):
		self.data = self.synx.get_data()
		self.ln = self.synx.get_ln()
		self.errs = self.synx.get_err()

		self.out = parsing_control(self.data, self.ln)
		self.errs += self.out[0]
		self.errs.sort()
		for er in self.errs:
			print(er)

		print(self.out[1])



	
def main():
	if len(sys.argv) != 2 :
		sys.exit("Usege: gaasm [name_file.txt]") #JAK PODANO ZŁE INFO, WYWALA NA STARCIE
	if sys.argv[1] == "/?":
		sys.exit("Compiler Grasol Architecture Asembler (gaasm) v? . Grasol 2019\nInstruction manual is on website: https://github.com/Grasol/GAASM-Grasol-Architecture- 'Grasol_CPU_Manual.pdf'")

	infilename = sys.argv[1]
	with open(infilename) as f:
		data = f.read()

		f.close()
	
		asm = Assembler(data)
		asm.phase1()


if __name__ == "__main__":
	main()

