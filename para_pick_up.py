#!/usr/usc/bin/python
import sys
import os
import glob
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file",dest="filename",help="specify the file you want to process, *.mips means all the mips file in current dirctory")
parser.add_option("-p", "--para",dest="parameter",help="specify the parameter you want to get")
(options, args) = parser.parse_args()

parameter_list=options.parameter.split()

if "*" in options.filename:
	file_list=glob.glob(options.filename)
else:
	file_list=options.filename.split()
	

print "dir:",os.path.abspath('.')
print "file name\t",
for parameter in parameter_list:
	print parameter,"\t",
print " "



for filename in file_list:
	print filename,"\t",
	fp=open(filename)
	for line in fp.readlines():
		for parameter in parameter_list:
			if parameter in line:
				print line.split()[1],"\t",
	print " "
	fp.close()
