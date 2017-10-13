#!/usr/bin/python


import os, datetime, sys
import numpy as np




if __name__ == '__main__':

	var = ['tavg', 'tasmax', 'tasmin']
	
	rcp = ['rcp45', 'rcp85']
	
	imgsize = ['620', '1000', 'diy', 'hd', 'hdsd']

	for i in range(len(var)):
		for j in range(len(rcp)):
			for k in range(len(imgsize)):
				print var[i]+' '+imgsize[k]+' '+rcp[j]
				cmd = 'ls -lh ./Images/'+var[i]+'/'+imgsize[k]+'/*'+rcp[j]+'* | wc -l'
				os.system(cmd)
				