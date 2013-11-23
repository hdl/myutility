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

def get_detai(cache_size,line_size,assoc,read_ports,write_ports,nr_bits_read_out,tagbits):
	'''The parameters are:
	   cache_size, line_size,assoc,read_ports, write_ports, nr_bits_read_out, tagbits
	   They are string
	   nr_bits_read_out may casue exception, but this function can recursion
	   tagbits is 30 for L1Data, 29 forL1L, 26for L2 
	'''
	url = 'http://quid.hpl.hp.com:9081/cacti/detailed.y'  
	values = {'cache_size' : cache_size,  
	          'line_size' : line_size,
	          'assoc' : assoc,  
	          'nrbanks' : '1',
	          'technode' : '32',
			  'rwports' : '0',
	          'read_ports' : read_ports,
	          'write_ports' : write_ports,
			  'ser_ports' : '0',
	          'output' : nr_bits_read_out, #maybe cause exception
			  'changetag' : '1',
			  'tagbits' : tagbits, #30 for L1Data, 29 forL1L, 26for L2
			  'access_mode' : '0',
			  'temp' : '360',
	          'data_arr_ram_cell_tech_flavor_in' : '0',
	          'data_arr_periph_global_tech_flavor_in' : '0',
	          'tag_arr_ram_cell_tech_flavor_in' : '0',
	          'tag_arr_periph_global_tech_flavor_in' : '0',
	          'interconnect_projection_type_in' : '1',
			  'wire_outside_mat_type_in' : '0',
	          'action' : 'submit',
	          'cacti' : 'cache',  
	          'detailed' : 'detailed_cache',
	          'preview-article' : 'Submit' }  
	
	data = urllib.urlencode(values) # encode
	req = urllib2.Request(url, data)  # send request
	response = urllib2.urlopen(req)  # receive
	the_page = response.read()  #read
	if the_page.find('Exception') == -1 :
		if len(re.findall(r"Access time \(ns\): (.+?)<br>",the_page)) == 1 :
			return re.findall(r"Access time \(ns\): (.+?)<br>",the_page)[0]
		else:
			return get_detai(cache_size,line_size,assoc,rwports,read_ports,write_ports,nr_bits_read_out,tagbits)
	else : 
		nr_int=int(nr_bits_read_out)
		nr_int = nr_int -1
		nr_bits_read_out=str(nr_int)
		print "cache recursion for nr_bits_read_out--"
		return get_detai(cache_size,line_size,assoc,rwports,read_ports,write_ports,nr_bits_read_out,tagbits)	
		
def get_sram(cache_size,read_ports,write_ports,nr_bits_read_out):
	'''The parameters are:
	   cache_size, read_ports, write_ports, nr_bits_read_out
		nr_bits_read_out may casue exception, but this function can recursion
	   They are string
	'''
	url = 'http://quid.hpl.hp.com:9081/cacti/sram.y'  
	values = {'cache_size' : cache_size,  
	          'nrbanks' : '1',
			  'rwports' : '0',
	          'read_ports' : read_ports,
	          'write_ports' : write_ports,
			  'ser_ports' : '0',
	          'output' : nr_bits_read_out,
			  'technode' : '32',
			  'temp' : '360',
	          'data_arr_ram_cell_tech_flavor_in' : '0',
	          'data_arr_periph_global_tech_flavor_in' : '0',
	          'tag_arr_ram_cell_tech_flavor_in' : '0',
	          'tag_arr_periph_global_tech_flavor_in' : '0',
	          'interconnect_projection_type_in' : '1',
			  'wire_outside_mat_type_in' : '0',
	          'action' : 'submit',
	          'cacti' : 'cache',  
	          'pure_sram' : 'pure_sram',
	          'preview-article' : 'Submit' }  
	
	data = urllib.urlencode(values) # encode
	req = urllib2.Request(url, data)  # send request
	response = urllib2.urlopen(req)  # receive
	the_page = response.read()  #read
	if the_page.find('Exception') == -1 :
		if len(re.findall(r"Access time \(ns\): (.+?)<br>",the_page)) == 1 :
			return re.findall(r"Access time \(ns\): (.+?)<br>",the_page)[0]
		else:
			return get_sram(cache_size,read_ports,write_ports,nr_bits_read_out)
	else : 
		nr_int=int(nr_bits_read_out)
		nr_int = nr_int-1
		nr_bits_read_out=str(nr_int)
		print "sram recursion for nr_bits_read_out--"
		return get_sram(cache_size,read_ports,write_ports,nr_bits_read_out)



def replace(filename,l1inst_int,l1data_int,l2inst_int,l2data_int,l2inst_null_str):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(filename)
    for line in old_file:
        if("-cache:il1lat" in line):
            line ="-cache:il1lat	"+str(l1inst_int)+"\n" 
        if("-cache:dl1lat" in line):
			line ="-cache:dl1lat	"+str(l1data_int)+"\n" 
        if("-cache:il2lat" in line):
            line ="-cache:il2lat	"+str(l2inst_int)+"\n" 
        if("-cache:dl2lat" in line):
			line ="-cache:dl2lat	"+str(l2data_int)+"\n"
        if(l2inst_null_str=="NULL" and "-cache:il2  " in line):
			line ="-cache:il2							dl2 \n"
        new_file.write(line)
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(filename)
    #Move new file
    move(abs_path, filename)


def add_to_file(filename_list,l1inst_int,l1data_int,l2inst_int,l2data_int,l2inst_null_str):
	print "modify latencies for the follwing files:"
	for filename in filename_list:
		print filename 
		replace(filename,l1inst_int,l1data_int,l2inst_int,l2data_int,l2inst_null_str)

def add_ram_time_to_cfg(filename_list,sram_access_time):
	print "append ram_access_time for the follwing files:"
	for filename in filename_list:
		print filename
		open(filename,"a+b").write("\n\n#ram_access_time			"+sram_access_time)
def get_min_int(float_a):
	int_a=int(float_a)
	if (float_a-int_a > 0):
		return int_a+1
	else:
		return int_a

def i_cache(sets,bsize,assoc,ifqsize):
	cache_size=str(int(sets)*int(bsize)*int(assoc))
	line_size=bsize
	wr_ports=str(get_min_int(float(ifqsize)*4/float(bsize)))
	nr_bits=str(int(bsize)*8)
	list=(cache_size,line_size,wr_ports,nr_bits)
	return list
def main():

	parser = OptionParser()
	
	parser.add_option("-a", "--l1inst",dest="l1inst",help="sets, bsize, assoc")
	parser.add_option("-b", "--l1data",dest="l1data",help="")
	parser.add_option("-c", "--l2inst",dest="l2inst",help="can be NULL")
	parser.add_option("-d", "--l2data",dest="l2data",help="")
	parser.add_option("-r", "--ruu",dest="ruu",help="ialu, imult, fpalu, fpmult")
	parser.add_option("-s", "--share", dest="share", help="memport, ifqsize, issue_width, decode_width")
	#parser.add_option("-f", "--filename",dest="filename",help="add the result to the specified files")
	(options, args) = parser.parse_args()	
	
	if(type(options.l1inst)==type(None)):
		print "usage: -h"
		return 0

	
	l1inst_list=options.l1inst.split()
	#l1data_list=options.l1data.split()
	#l2inst_list=options.l2inst.split()
	#l2data_list=options.l2data.split()
	#ruu_list=options.ruu.split()
	share_list=options.share.split()

	#i_cache(sets,bsize,assoc,ifqsize) 
	print i_cache(l1inst_list[0],l1inst_list[1],l1inst_list[2],share_list[1])	

	



if __name__ == '__main__':
    main()
