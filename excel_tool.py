#!/usr/usc/python/2.6.1/bin/python
import xdrlib
import sys
import os
import xlrd
import xlwt


#read read

file = xlrd.open_workbook('estimator.xls')
sheet1 = file.sheet_by_name(u'ConfigFileParams')

cell_decode_width= sheet1.cell_value(10,1) #B11
print "decode_width is",cell_decode_width
cell_issue_width= sheet1.cell_value(11,1) #B12


print "issue_width is",cell_issue_width

sheet3 = file.sheet_by_name(u'Port Calculation')

cell_ruu_read_port = sheet3.cell_value(17,1) #B18
cell_ruu_write_port = sheet3.cell_value(18,1) #B19

print "ruu read port is",cell_ruu_read_port
print "ruu write port is",cell_ruu_write_port
