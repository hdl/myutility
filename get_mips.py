#!/usr/usc/python/2.6.1/bin/python
import urllib  
import urllib2 
import re
import sys
import os
import glob
from optparse import OptionParser
from tempfile import mkstemp
from shutil import move
from os import remove, close

art_inst=""
art_cycle=""
twolf_cycle=""
twolf_inst=""
mcf_cycle=""
mcf_inst=""
applu_cycle=""
applu_inst=""

def get_inst_cycle(filename_list):
	global art_inst
	global art_cycle
	global twolf_cycle
	global twolf_inst
	global mcf_cycle
	global mcf_inst
	global applu_cycle
	global applu_inst
	for filename in filename_list:
		if "art" in filename:
			fp=open(filename)
			for line in fp.readlines():
				if "sim_num_insn" in line:
					art_inst=line.split()[1]
					print art_inst
				elif "sim_cycle" in line:
					art_cycle=line.split()[1]
			fp.close()
		elif "twolf" in filename:
			fp=open(filename)
			for line in fp.readlines():
				if "sim_num_insn" in line:
					twolf_inst=line.split()[1]
				elif "sim_cycle" in line:
					twolf_cycle=line.split()[1]
			fp.close()
		elif "mcf" in filename:
			fp=open(filename)
			for line in fp.readlines():
				if "sim_num_insn" in line:
					mcf_inst=line.split()[1]
				elif "sim_cycle" in line:
					mcf_cycle=line.split()[1]
			fp.close()
		elif "applu" in filename:
			fp=open(filename)
			for line in fp.readlines():
				if "sim_num_insn" in line:
					applu_inst=line.split()[1]
				elif "sim_cycle" in line:

					applu_cycle=line.split()[1]
			fp.close()
		else:
			print "no keywords: art, twolf, mcf, applu are not in your filenames"
			exit(-1)
			
def print_inst_cycle(filename_list):
	global art_inst
	global art_cycle
	global twolf_cycle
	global twolf_inst
	global mcf_cycle
	global mcf_inst
	global applu_cycle
	global applu_inst
	print "The files are:"
	for filename in filename_list:
		print filename
	print ""
	print "the results are: \nbench	insts		cycles"
	print "art	%s	%s"%(art_inst,art_cycle)
	print "twolf	%s	%s"%(twolf_inst,twolf_cycle)
	print "mcf	%s	%s"%(mcf_inst,mcf_cycle)
	print "applu	%s	%s"%(applu_inst,applu_cycle)
	print ""
def main():

	parser = OptionParser()
	#parser.add_option("-a", "--l1inst",dest="l1inst",help="cache_size, line_size,assoc,read_ports, write_ports, nr_bits_read_out")
	parser.add_option("-t", "--time",dest="time",help="time of per cycle, ns")
	parser.add_option("-f", "--filename_list",dest="filename_list",help="make sure your 4 files share same part name, then use -f \"*___.___\"")
	(options, args) = parser.parse_args()	
	
	filename_list=glob.glob(options.filename_list)
	
	get_inst_cycle(filename_list)
	print_inst_cycle(filename_list)

	print "the time per cycles you input is %s(ns)"%(options.time)
	cycles=int(art_cycle)+int(twolf_cycle)+int(mcf_cycle)+int(applu_cycle)
	insts=int(art_inst)+int(twolf_inst)+int(mcf_inst)+int(applu_inst)
	print "MIPS:	",
	print float(insts)/float(cycles)/float(options.time)**(-9)

if __name__ == '__main__':
    main()
