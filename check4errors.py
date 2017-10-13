#!/work/anaconda2/bin/python

'''
	Example Usage:
	check4errors.py "model" "rcp" "var" "enviroment"
	
	where,
	model 		=	Any of the GCM's
	rcp			=	either rcp45 or rcp85 (the two preferred carbon pathways)
	var			= 	either tavg, tasmax, pr tasmin
	enviroment	=	local or S3, depending on the "state" of processing
					i.e., have earlier results already been moved over to S3...
	
	
'''

import os, datetime, sys, subprocess, glob



if __name__ == '__main__':
	
	model = sys.argv[1]
	rcp = sys.argv[2]
	var = sys.argv[3]
	enviro = sys.argv[4]
	
	
	mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	
	if(enviro == 'S3'):
		cmd = 'ls /mnt/ds-s3LOCA/'+model+'/daily_by_month/*'+var+'*'+rcp+'* | wc -l'
	if(enviro == 'local'):
		cmd = 'ls ./daily_by_month/*'+rcp+'* | wc -l'
	
	nfiles = os.popen(cmd).read().split(' ')[0]
	print model+'-'+rcp+': '+nfiles.split('\n')[0]+' files'
	
	yyyy = 2020
	for i in range(80):
		if(i != 0): yyyy+=1
		for j in range(len(mons)):
			if(enviro == 'S3'):
				file = '/mnt/ds-s3LOCA/'+model+'/daily_by_month/'+mons[j]+'_'+str(yyyy)+'_daily_tavg_'+model+'_'+rcp+'.nc'
			if(enviro == 'local'):
				file = './daily_by_month/'+mons[j]+'_'+str(yyyy)+'_daily_tavg_'+model+'_'+rcp+'.nc'
			fchk = os.path.isfile(file)
			if(str(fchk) != 'True'): print file+' was not processed'
			if(str(fchk) == 'True'):
				cmd = 'stat '+file+' | grep "Size"'
				fsiz = os.popen(cmd).read().split(':')[1].split(' ')[1]
				if(int(fsiz) < 50000000):
					print file+' is corrupted'
			
	
