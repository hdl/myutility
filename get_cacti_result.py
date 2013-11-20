#!/usr/usc/python/2.6.1/bin/python
import urllib  
import urllib2 
import re
import sys
import os
import glob
from optparse import OptionParser
import fileinput

def get_normal(cache_size,line_size,assoc,nrbanks,technode):
	url = 'http://quid.hpl.hp.com:9081/cacti/index.y'  
	values = {'cache_size' : cache_size,  
	          'line_size' : line_size,
	          'assoc' : assoc,  
	          'nrbanks' : nrbanks,
	          'technode' : technode,  
	          'action' : 'submit',
	          'cacti' : 'cache',  
	          'simple' : 'simple_cache',
	          'preview-article' : 'Submit' }  
	
	data = urllib.urlencode(values) # encode
	req = urllib2.Request(url, data)  # send request
	response = urllib2.urlopen(req)  # receive
	the_page = response.read()  #read
	return the_page

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
		print "recursion"
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
		print "recursion"
		return get_sram(cache_size,read_ports,write_ports,nr_bits_read_out)
def get_min_int(float_a):
	int_a=int(float_a)
	if (float_a-int_a > 0):
		return int_a+1
	else:
		return int_a

def replaceline(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def add_to_file(filename_list,l1inst_int,l1data_int,l2inst_int,l2data_int):
	for filename in filename_list:
		replaceline(filename,"-cache:dl1lat$","-cache:dl1lat "+str(l1data_int))

def main():

	parser = OptionParser()
	parser.add_option("-a", "--l1inst",dest="l1inst",help="cache_size, line_size,assoc,read_ports, write_ports, nr_bits_read_out")
	parser.add_option("-b", "--l1data",dest="l1data",help="")
	parser.add_option("-c", "--l2inst",dest="l2inst",help="")
	parser.add_option("-d", "--l2data",dest="l2data",help="")
	parser.add_option("-s", "--sram",dest="sram",help="cache_size, read_ports, write_ports, nr_bits_read_out")
	parser.add_option("-f", "--filename",dest="filename",help="add the result to the specified files")

	(options, args) = parser.parse_args()	

	l1inst_list=options.l1inst.split()
	l1data_list=options.l1data.split()
	l2inst_list=options.l2inst.split()
	l2data_list=options.l2data.split()
	sram_list=options.sram.split()

	l1inst_access_time=get_detai(l1inst_list[0],l1inst_list[1],l1inst_list[2] ,l1inst_list[3] ,l1inst_list[4],l1inst_list[5],'29') 
	l1data_access_time=get_detai(l1data_list[0],l1data_list[1],l1data_list[2] ,l1data_list[3] ,l1data_list[4],l1data_list[5],'30') 
	l2inst_access_time=get_detai(l2inst_list[0],l2inst_list[1],l2inst_list[2] ,l2inst_list[3] ,l2inst_list[4],l2inst_list[5],'28') 
	if l2data_list[0]=='NULL' :
		l2data_access_time=l2inst_access_time
	else:
		l2data_access_time=get_detai(l2data_list[0],l2data_list[1],l2data_list[2] ,l2data_list[3] ,l2data_list[4],l2data_list[5],'28') 
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

	if(options.filename!="NULL"):
		add_to_file(options.filename,l1inst_int,l1data_int,l2inst_int,l2data_int)
	else:
		print "no files need to add"

if __name__ == '__main__':
    main()
