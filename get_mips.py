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
			print "get art form", filename
			fp=open(filename)
			for line in fp.readlines():
				if "sim_num_insn" in line:
					art_inst=line.split()[1]
				elif "sim_cycle" in line:
					art_cycle=line.split()[1]
			fp.close()
		elif "twolf" in filename:
			print "get twolf form", filename
			fp=open(filename)
			for line in fp.readlines():
				if "sim_num_insn" in line:
					twolf_inst=line.split()[1]
				elif "sim_cycle" in line:
					twolf_cycle=line.split()[1]
			fp.close()
		elif "mcf" in filename:
			print "get mcf form", filename
			fp=open(filename)
			for line in fp.readlines():
				if "sim_num_insn" in line:
					mcf_inst=line.split()[1]
				elif "sim_cycle" in line:
					mcf_cycle=line.split()[1]
			fp.close()
		elif "applu" in filename:
			print "get applu form", filename
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

	print "art_inst:		%s"%(art_inst)
	print "art_cycle:		%s"%(art_cycle)
	print "art_inst/cycle:		%s"%(str(float(art_inst)/float(art_cycle)))

	print "twolf_inst:		%s"%(twolf_inst)
	print "twolf_cycle:		%s"%(twolf_cycle)
	print "twolf_inst/cycle:	%s"%(str(float(twolf_inst)/float(art_cycle)))

	print "mcf_inst:		%s"%(mcf_inst)
	print "mcf_cycle:		%s"%(mcf_cycle)
	print "mcf_inst/cycle:	%s"%(str(float(mcf_inst)/float(mcf_cycle)))

	print "applu_inst:		%s"%(applu_inst)
	print "applu_cycle:		%s"%(applu_cycle)
	print "applu_inst/cycle:	%s"%(str(float(applu_inst)/float(applu_cycle)))
	

def get_ram_access_time(filename):
	fp=open(filename)
	for line in fp.readlines():
		if "#ram_access_time" in line:
			return float(line.split()[1])
			fp.close()


def main():

	parser = OptionParser()
	#parser.add_option("-a", "--l1inst",dest="l1inst",help="cache_size, line_size,assoc,read_ports, write_ports, nr_bits_read_out")
	parser.add_option("-t", "--time",dest="time",help="time of per cycle, ns or your .cfg file which include ram access time")
	parser.add_option("-f", "--filename_list",dest="filename_list",help="make sure your 4 files share same part name, then use -f \"*___.___\"")
	(options, args) = parser.parse_args()	
	
	filename_list=glob.glob(options.filename_list)
	time_ns_str=options.time

	get_inst_cycle(filename_list)
	print_inst_cycle(filename_list)
	
	cycles=int(art_cycle)+int(twolf_cycle)+int(mcf_cycle)+int(applu_cycle)
	insts=int(art_inst)+int(twolf_inst)+int(mcf_inst)+int(applu_inst)	
	print "sum(insts)/sum(cycles):  ",float(insts)/float(cycles)
	print ""

	

	if type(options.time)==type(None):
		print "Have no options for time, quit"
		return 0
	elif ".cfg" in options.time:
		print "use ram_access_time in file %s"%options.time
		ram_access_time=get_ram_access_time(options.time)

		print "the time is(ns) ",ram_access_time 
		print "art_mips:		",float(art_inst)/float(art_cycle)/ram_access_time*(10**3)
		print "twolf_mips:		",float(twolf_inst)/float(twolf_cycle)/ram_access_time*(10**3)
		print "mcf_mips:		",float(mcf_inst)/float(mcf_cycle)/ram_access_time*(10**3)
		print "applu_mips:		",float(applu_inst)/float(applu_cycle)/ram_access_time*(10**3)
		print "MIPS:		",float(insts)/float(cycles)/ram_access_time*(10**3)
	else:
		print "use access time you input %s(ns)"%(options.time)
		ram_access_time=float(options.time)
		
		print "the time is(ns) ",ram_access_time 
		print "art_mips:		",float(art_inst)/float(art_cycle)/ram_access_time*(10**3)
		print "twolf_mips:		",float(twolf_inst)/float(twolf_cycle)/ram_access_time*(10**3)
		print "mcf_mips:		",float(mcf_inst)/float(mcf_cycle)/ram_access_time*(10**3)
		print "applu_mips:		",float(applu_inst)/float(applu_cycle)/ram_access_time*(10**3)
		print "MIPS:		",float(insts)/float(cycles)/ram_access_time*(10**3)

if __name__ == '__main__':
    main()
