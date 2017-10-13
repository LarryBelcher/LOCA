#!/work/anaconda2/bin/python


import os, datetime, sys, subprocess, glob



if __name__ == '__main__':
	
	model = sys.argv[1]
	var = sys.argv[2]
	
	rcp = ['rcp45','rcp85']
	
	for r in range(2):
	
		files = glob.glob('/mnt/ds-s3LOCA/'+model+'/decade/*'+var+'*'+rcp[r]+'*')
		rem = 96 - int(len(files))
		if(len(files) != 96): print model+' '+rcp[r]+' '+var+' processing is incomplete, '+str(rem)+' files to go'
		
		gf = 0
		for i in range(len(files)):
			cmd = 'stat '+files[i]+' | grep "Size"'
			fsiz = os.popen(cmd).read().split(':')[1].split(' ')[1]
			if(int(fsiz) < 1900000):
				print files[i]+' is corrupted'
			if(int(fsiz) > 1900000): 
				gf+=1
		if(gf == 96): print str(gf)+' files have been processed for '+model+' '+var+' '+rcp[r]

