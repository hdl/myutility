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
from math import log

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
			print "no acees time string find, retry"
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
	i_cache_list=(cache_size,line_size,assoc,wr_ports,wr_ports,nr_bits)
	return i_cache_list

def d_cache(sets, bsize, assoc, memport):
	cache_size=str(int(sets)*int(bsize)*int(assoc))
	line_size=bsize
	wr_ports=memport
	nr_bits=str(int(bsize)*8)
	d_cache_list=(cache_size,line_size,assoc,wr_ports,wr_ports,nr_bits)
	return d_cache_list

def ruu(ruu_size, ialu, imult, fpalu, fpmult, memport, ifqsize, issue_width, decode_width):
	ruu_read_port = (int(ialu)+int(imult)+int(fpalu)+int(fpmult)+int(ifqsize)+int(issue_width))
	ruu_write_port = (int(ialu)+int(imult)+int(fpalu)+int(fpmult)+int(decode_width))
	BitPerRegId=6
	WordInBit=32
	BitPerPC=32
	temp=int(ialu)+int(imult)+int(fpalu)+int(fpmult)+int(memport)
	BitPerExUId=get_min_int(log(temp,2))
	BitPerRuuEnt=3 * (BitPerRegId + WordInBit + 1) + BitPerPC + BitPerExUId + 2
	cache_size = int(ruu_size)*BitPerRuuEnt/8
	ruu_list=(str(cache_size),str(ruu_read_port),str(ruu_write_port),str(BitPerRuuEnt))
	return ruu_list

def gen_content_list(options,l1inst_int,l1data_int,l2inst_int,l2data_int,sram_access_time):
	
	l1inst_list=options.l1inst.split()
	l1data_list=options.l1data.split()
	l2data_list=options.l2data.split()

	if options.l2inst=="dl2":
		l2inst_list=l2data_list
	else:
		l2inst_list=options.l2inst.split()
	ruu_list=options.ruu.split()

	share_list=options.share.split()

	content_list = []
	content_list.append(ruu_list[1]) #ifqsize
	content_list.append(share_list[3])
	content_list.append(share_list[2])
	content_list.append(ruu_list[0])
	content_list.append("dl1:"+l1data_list[0]+":"+l1data_list[1]+":"+l1data_list[2]+":"+l1data_list[3])
	content_list.append(str(l1data_int))
	content_list.append("ul2:"+l2data_list[0]+":"+l2data_list[1]+":"+l2data_list[2]+":"+l2data_list[3])
	content_list.append(str(l2data_int))
	content_list.append("il1:"+l1inst_list[0]+":"+l1inst_list[1]+":"+l1inst_list[2]+":"+l1inst_list[3])
	content_list.append(str(l1inst_int))
	content_list.append("dl2")
	content_list.append(str(l2inst_int))
	content_list.append(ruu_list[1])	
	content_list.append(ruu_list[2])
	content_list.append(share_list[0])
	content_list.append(ruu_list[2])
	content_list.append(ruu_list[3])
	content_list.append(sram_access_time) 
	return content_list
def main():

	parser = OptionParser()
	
	parser.add_option("-a", "--l1inst",dest="l1inst",help="sets, bsize, assoc, replace policy(l r f)")
	parser.add_option("-b", "--l1data",dest="l1data",help="")
	parser.add_option("-c", "--l2inst",dest="l2inst",help="can be dl2")
	parser.add_option("-d", "--l2data",dest="l2data",help="")
	parser.add_option("-r", "--ruu",dest="ruu",help="ruu_size, ialu, imult, fpalu, fpmult")
	parser.add_option("-s", "--share",dest="share", help="memport, ifqsize, issue_width, decode_width")
	parser.add_option("-f", "--filename",dest="filename", help="generate config file use this filename")
	(options, args) = parser.parse_args()	
	
	if(type(options.l1inst)==type(None)):
		print "example:"
		print '''python gen_config.py -a "256 32 2 l" -b "128 32 4 l" -c "1024 64 8 l" -d "1024 64 8 l" -r "32 2 1 1 1" -s "2 4 4 4" '''
		return 0

	
	l1inst_list=options.l1inst.split()
	l1data_list=options.l1data.split()
	l2data_list=options.l2data.split()

	if options.l2inst=="dl2":
		l2inst_list=l2data_list
	else:
		l2inst_list=options.l2inst.split()
	ruu_list=options.ruu.split()
	share_list=options.share.split()

	#i_cache(sets,bsize,assoc,ifqsize)
	#ruu(ruu_size,ialu, imult, fpalu, fpmult, ifqsize, issue_width, decode_width,memport)
	il1=i_cache(l1inst_list[0],l1inst_list[1],l1inst_list[2],share_list[1])	
	dl1=d_cache(l1data_list[0],l1data_list[1],l1data_list[2],share_list[0])
	il2=i_cache(l2inst_list[0],l2inst_list[1],l2inst_list[2],share_list[1])
	dl2=d_cache(l2data_list[0],l2data_list[1],l2data_list[2],share_list[0])
	ruu_detail=ruu(ruu_list[0],ruu_list[1],ruu_list[2],ruu_list[3],ruu_list[4],share_list[0],share_list[1],share_list[2],share_list[3])
	
	l1inst_access_time=get_detai(il1[0],il1[1],il1[2],il1[3],il1[4],il1[5], '29')
	l1data_access_time=get_detai(dl1[0],dl1[1],dl1[2],dl1[3],dl1[4],dl1[5], '30')
	l2inst_access_time=get_detai(il2[0],il2[1],il2[2],il2[3],il2[4],il2[5], '26')
	l2data_access_time=get_detai(dl2[0],dl2[1],dl2[2],dl2[3],dl2[4],dl2[5], '26')
	sram_access_time=get_sram(ruu_detail[0],ruu_detail[1],ruu_detail[2],ruu_detail[3])

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
	
	content_list = gen_content_list(options,l1inst_int,l1data_int,l2inst_int,l2data_int,sram_access_time)
	print content_list
	print len(content_list)
	filecontent='''
# load configuration from a file
# -config               

# dump configuration to a file
# -dumpconfig           

# print help message
# -h                          false 

# verbose operation
# -v                          false 

# enable debug message
# -d                          false 

# start in Dlite debugger
# -i                          false 

# random number generator seed (0 for timer seed)
-seed                             1 

# initialize and terminate immediately
# -q                          false 

# restore EIO trace execution from <fname>
# -chkpt                     <null> 

# redirect simulator output to file (non-interactive only)
# -redir:sim                 <null> 

# redirect simulated program output to file
# -redir:prog                <null> 

# simulator scheduling priority
-nice                             0 

# maximum number of inst's to execute
-max:inst                         0 

# number of insts skipped before timing starts
-fastfwd                          0 

# generate pipetrace, i.e., <fname|stdout|stderr> <range>
# -ptrace                    <null> 

# instruction fetch queue size (in insts)
-fetch:ifqsize                    %s 

# extra branch mis-prediction latency
-fetch:mplat                      3 

# speed of front-end of machine relative to execution core
-fetch:speed                      1 

# branch predictor type {nottaken|taken|perfect|bimod|2lev|comb}
-bpred                        bimod 

# bimodal predictor config (<table size>)
-bpred:bimod           2048 

# 2-level predictor config (<l1size> <l2size> <hist_size> <xor>)
-bpred:2lev            1 1024 8 0 

# combining predictor config (<meta_table_size>)
-bpred:comb            1024 

# return address stack size (0 for no return stack)
-bpred:ras                        8 

# BTB config (<num_sets> <associativity>)
-bpred:btb             512 4 

# speculative predictors update in {ID|WB} (default non-spec)
# -bpred:spec_update         <null> 

# instruction decode B/W (insts/cycle)
-decode:width                     %s 

# instruction issue B/W (insts/cycle)
-issue:width                      %s 

# run pipeline with in-order issue
-issue:inorder                false 

# issue instructions down wrong execution paths
-issue:wrongpath               true 

# instruction commit B/W (insts/cycle)
-commit:width                     4 

# register update unit (RUU) size
-ruu:size                        %s 

# load/store queue (LSQ) size
-lsq:size                         8 

# l1 data cache config, i.e., {<config>|none}
-cache:dl1             %s 

# l1 data cache hit latency (in cycles)
-cache:dl1lat                     %s 

# l2 data cache config, i.e., {<config>|none}
-cache:dl2             %s 

# l2 data cache hit latency (in cycles)
-cache:dl2lat                     %s 

# l1 inst cache config, i.e., {<config>|dl1|dl2|none}
-cache:il1              %s

# l1 instruction cache hit latency (in cycles)
-cache:il1lat                     %s 

# l2 instruction cache config, i.e., {<config>|dl2|none}
-cache:il2                      %s 

# l2 instruction cache hit latency (in cycles)
-cache:il2lat                     %s 

# flush caches on system calls
-cache:flush                  false 

# convert 64-bit inst addresses to 32-bit inst equivalents
-cache:icompress              false 

# memory access latency (<first_chunk> <inter_chunk>)
-mem:lat               18 2 

# memory access bus width (in bytes)
-mem:width                        8 

# instruction TLB config, i.e., {<config>|none}
-tlb:itlb              itlb:16:4096:4:l 

# data TLB config, i.e., {<config>|none}
-tlb:dtlb              dtlb:32:4096:4:l 

# inst/data TLB miss latency (in cycles)
-tlb:lat                         30 

# total number of integer ALU's available
-res:ialu                         %s 

# total number of integer multiplier/dividers available
-res:imult                        %s 

# total number of memory system ports available (to CPU)
-res:memport                      %s

# total number of floating point ALU's available
-res:fpalu                        %s 

# total number of floating point multiplier/dividers available
-res:fpmult                       %s 

# profile stat(s) against text addr's (mult uses ok)
# -pcstat                    <null> 

# operate in backward-compatible bugs mode (for testing only)
-bugcompat                    false

#ram_access_time                  %s 
	'''%tuple(content_list) 	
	fp=open(options.filename,'w')
	fp.write(filecontent)
	fp.close()
	print "generate file:	",options.filename


if __name__ == '__main__':
    main()
