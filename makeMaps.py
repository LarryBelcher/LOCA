#!/usr/bin/python


import os, datetime, sys, glob
import numpy as np




if __name__ == '__main__':

	#var = ['tavg', 'tasmax', 'tasmin']
	var = ['tasmin']
	
	#mm = ['1','2','3','4','5','6','7','8','9','10','11','12']	
	mm = ['0']
	
	dec = ['2020','2030','2040','2050','2060','2070','2080','2090']
	#dec = ['2020']
	
	rcp = ['rcp45', 'rcp85']
	
	imgsize = ['620', '1000', 'DIY', 'HD', 'HDSD']
	


	for i in range(len(var)):
		for j in range(len(mm)):
			for k in range(len(dec)):
				for l in range(len(rcp)):
					for m in range(len(imgsize)):
			
						if(mm[j] == '1'): mms = 'January'
						if(mm[j] == '2'): mms = 'February'
						if(mm[j] == '3'): mms = 'March'
						if(mm[j] == '4'): mms = 'April'
						if(mm[j] == '5'): mms = 'May'
						if(mm[j] == '6'): mms = 'June'
						if(mm[j] == '7'): mms = 'July'
						if(mm[j] == '8'): mms = 'August'
						if(mm[j] == '9'): mms = 'September'
						if(mm[j] == '10'): mms = 'October'
						if(mm[j] == '11'): mms = 'November'
						if(mm[j] == '12'): mms = 'December'
						
						#fpath = './Images/'+var[i]+'/'+imgsize[m].lower()+'/*'+mms+'*'+dec[k]+'*'+rcp[l]+'*'
						#file = glob.glob(fpath)
						#if(len(file) == 0):
						if(mm[0] == '0'):
							cmd = "python ./LocaDriver.py "+var[i]+" "+mm[j]+" "+dec[k]+" "+rcp[l]+" "+imgsize[m]
							os.system(cmd)