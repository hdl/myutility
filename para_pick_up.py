#!/usr/usc/bin/python
import sys
import os
import glob
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file",dest="filename",help="specify the file you want to process, *.mips means all the mips file in current dirctory")
parser.add_option("-p", "--para",dest="parameter",help="specify the parameter you want to get. If this is not specified, it's MIPS art_mips twolf_mips mcf_mips applu_mips")
(options, args) = parser.parse_args()

if type(options.parameter)==type(None):
	parameter_list=("MIPS:", "art_mips", "twolf_mips", "mcf_mips", "applu_mips")
else:
	parameter_list=options.parameter.split()

if "*" in options.filename:
	file_list=glob.glob(options.filename)
else:
	file_list=options.filename.split()
	

print "dir:",os.path.abspath('.')
print "file name\t",

fp=open(file_list[0])
for line in fp.readlines():
	for parameter in parameter_list:
		if parameter in line:
			print parameter,"\t",
print " "
fp.close()



for filename in file_list:
	print filename,"\t",
	fp=open(filename)
	for line in fp.readlines():
		for parameter in parameter_list:
			if parameter in line:
				print line.split()[1],"\t",
	print " "
	fp.close()
