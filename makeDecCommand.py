#!/work/anaconda2/bin/python


import os, datetime, sys, subprocess, glob



if __name__ == '__main__':
	
	model = sys.argv[1]
	var = sys.argv[2]
	
	rcp = ['rcp45','rcp85']
	
	for i in range(2):
		cmd = 'python decadeAvg.py '+model+' '+rcp[i]+' '+var+' >& '+model+'_decade_'+var+'_'+rcp[i]+' &'
		print cmd