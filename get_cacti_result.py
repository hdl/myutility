import urllib  
import urllib2 
import re
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

def main():
	the_result = get_sram('616','7','6','154')
	print "Sram Access time:", the_result

	the_result= get_detai('16384','32','2','1','1','256','29')
	print "L1 instruction:", the_result
	#cache_size, line_size,assoc,read_ports, write_ports, nr_bits_read_out, tagbits 


if __name__ == '__main__':
    main()
