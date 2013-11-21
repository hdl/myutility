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

	
def get_mips(filename_list)
	for filename in filename_list:
		if "art" in filename:
			print "art:",
			fp=open(filename)
			





def main():

	parser = OptionParser()
	parser.add_option("-a", "--l1inst",dest="l1inst",help="cache_size, line_size,assoc,read_ports, write_ports, nr_bits_read_out")
	parser.add_option("-b", "--l1data",dest="l1data",help="")
	parser.add_option("-c", "--l2inst",dest="l2inst",help="can be NULL")
	parser.add_option("-d", "--l2data",dest="l2data",help="")
	parser.add_option("-s", "--sram",dest="sram",help="cache_size, read_ports, write_ports, nr_bits_read_out")
	parser.add_option("-f", "--filename",dest="filename",help="add the result to the specified files")
	parser.add_option("-e", "--example",dest="example",help='''get_cacti_result.py -a "16384 32 2 1 1 256" -b "16384 32 4 2 2 256" -c "NULL" -d "524288 64 8 2 2 512" -s "616 13 9 154" -f "*.cfg"''')
	(options, args) = parser.parse_args()	
	
	if(options.example!=""):
		print '''cache parameter seqence: cache_size, line_size,assoc,read_ports, write_ports, nr_bits_read_out 
sram parameter sequence: cache_size, read_ports, write_ports, nr_bits_read_out  	
get_cacti_result.py -a "16384 32 2 1 1 256" -b "16384 32 4 2 2 256" -c "NULL" -d "524288 64 8 2 2 512" -s "616 13 9 154" -f "*.cfg"'''
		return 0
	l1inst_list=options.l1inst.split()
	l1data_list=options.l1data.split()
	l2inst_list=options.l2inst.split()
	l2data_list=options.l2data.split()
	sram_list=options.sram.split()

	l1inst_access_time=get_detai(l1inst_list[0],l1inst_list[1],l1inst_list[2] ,l1inst_list[3] ,l1inst_list[4],l1inst_list[5],'29') 
	l1data_access_time=get_detai(l1data_list[0],l1data_list[1],l1data_list[2] ,l1data_list[3] ,l1data_list[4],l1data_list[5],'30') 
	l2data_access_time=get_detai(l2data_list[0],l2data_list[1],l2data_list[2] ,l2data_list[3] ,l2data_list[4],l2data_list[5],'28') 
	
	if l2inst_list[0]=='NULL' :
		l2inst_access_time=l2data_access_time
	else:
	    l2inst_access_time=get_detai(l2inst_list[0],l2inst_list[1],l2inst_list[2] ,l2inst_list[3] ,l2inst_list[4],l2inst_list[5],'28') 
	
	sram_access_time=get_sram(sram_list[0],sram_list[1],sram_list[2] ,sram_list[3]) 
	
	print "L1inst:",l1inst_access_time	
	print "L1data:",l1data_access_time
	print "L2inst:",l2inst_access_time
	print "L2data:",l2data_access_time
	print "RuuRAM:",sram_access_time

	l1inst_float=float(l1inst_access_time)	
	l1data_float=float(l1data_access_time)
	l2inst_float=float(l2inst_access_time)
	l2data_float=float(l2data_access_time)
	sram_float=float(sram_access_time)

	l1inst_int=get_min_int(l1inst_float/sram_float)
	l1data_int=get_min_int(l1data_float/sram_float)
	l2inst_int=get_min_int(l2inst_float/sram_float)
	l2data_int=get_min_int(l2data_float/sram_float)	

	print "L1inst cycles:",l1inst_int	
	print "L1data cycles:",l1data_int
	print "L2inst cycles:",l2inst_int
	print "L2data cycles:",l2data_int
	print "RuuRAM cycles:",'1'

	if(options.filenamelist=="NULL"):
		print "no files need to add"
	elif("*." in options.filename):
		filename_list=glob.glob(options.filename)
		add_to_file(filename_list,l1inst_int,l1data_int,l2inst_int,l2data_int,l2inst_list[0])# the last one is l2 inst NULL option
	else:
		filename_list=options.filename.split() 
		add_to_file(filename_list,l1inst_int,l1data_int,l2inst_int,l2data_int,l2inst_list[0])# the last one is l2 inst NULL option
		

if __name__ == '__main__':
    main()
