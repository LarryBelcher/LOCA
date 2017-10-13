#!/work/anaconda2/bin/python

'''
	Example Usage:
	daily2daybymonth.py "model" "rcp" "var" "enviroment"
	
	where,
	model 		=	Any of the GCM's
	rcp			=	either rcp45 or rcp85 (the two preferred carbon pathways)
	var			= 	either tavg, tasmax, pr tasmin
	enviroment	=	local or S3, depending on the "state" of processing
					i.e., have earlier results already been moved over to S3...
	
'''

import os, sys, subprocess, glob, calendar
from datetime import datetime



if __name__ == '__main__':

	model = sys.argv[1]
	era = sys.argv[2]
	var = sys.argv[3]
	enviro = sys.argv[4]

	for i in range(1):
		
		if(model == 'ACCESS1-0'): mrun = 'r1i1p1'
		if(model == 'ACCESS1-3'): mrun = 'r1i1p1'
		if(model == 'bcc-csm1-1'): mrun = 'r1i1p1'
		if(model == 'bcc-csm1-1-m'): mrun = 'r1i1p1'
		if(model == 'CanESM2'): mrun = 'r1i1p1'
		if(model == 'CCSM4'): mrun = 'r6i1p1'
		if(model == 'CESM1-BGC'): mrun = 'r1i1p1'
		if(model == 'CESM1-CAM5'): mrun = 'r1i1p1'
		if(model == 'CMCC-CM'): mrun = 'r1i1p1'
		if(model == 'CMCC-CMS'): mrun = 'r1i1p1'
		if(model == 'CNRM-CM5'): mrun = 'r1i1p1'
		if(model == 'CSIRO-Mk3-6-0'): mrun = 'r1i1p1'
		if(model == 'EC-EARTH' and era == 'rcp45'): mrun = 'r8i1p1'
		if(model == 'EC-EARTH' and era == 'rcp85'): mrun = 'r2i1p1'
		if(model == 'FGOALS-g2'): mrun = 'r1i1p1'
		if(model == 'GFDL-CM3'): mrun = 'r1i1p1'
		if(model == 'GFDL-ESM2G'): mrun = 'r1i1p1'
		if(model == 'GFDL-ESM2M'): mrun = 'r1i1p1'
		if(model == 'GISS-E2-H' and era == 'historical'): mrun = 'r6i1p1'
		if(model == 'GISS-E2-H' and era == 'rcp45'): mrun = 'r6i1p3'
		if(model == 'GISS-E2-H' and era == 'rcp85'): mrun = 'r2i1p1'
		if(model == 'GISS-E2-R' and era == 'historical'): mrun = 'r6i1p1'
		if(model == 'GISS-E2-R' and era == 'rcp45'): mrun = 'r6i1p1'
		if(model == 'GISS-E2-R' and era == 'rcp85'): mrun = 'r2i1p1'				
		if(model == 'HadGEM2-AO'): mrun = 'r1i1p1'
		if(model == 'HadGEM2-CC'): mrun = 'r1i1p1'
		if(model == 'HadGEM2-ES'): mrun = 'r1i1p1'
		if(model == 'inmcm4'): mrun = 'r1i1p1'
		if(model == 'IPSL-CM5A-LR'): mrun = 'r1i1p1'
		if(model == 'IPSL-CM5A-MR'): mrun = 'r1i1p1'								
		if(model == 'MIROC5'): mrun = 'r1i1p1'
		if(model =='MIROC-ESM'): mrun = 'r1i1p1'
		if(model == 'MIROC-ESM-CHEM'): mrun = 'r1i1p1'
		if(model == 'MPI-ESM-LR'): mrun = 'r1i1p1'
		if(model == 'MPI-ESM-MR'): mrun = 'r1i1p1'
		if(model == 'MRI-CGCM3'): mrun = 'r1i1p1'
		if(model == 'NorESM1-M'): mrun = 'r1i1p1'
		

		
		mm = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		for j in range(80):
			year = j+2020
			yyyy = str(year)
			srch = yyyy
			
			
			if(var == 'tasmax'):
				files = glob.glob('/mnt/s3-LOCA/'+model+'/16th/'+era+'/'+mrun+'/tasmax/*_'+srch+'*')
			
			if(var == 'tasmin'):
				files = glob.glob('/mnt/s3-LOCA/'+model+'/16th/'+era+'/'+mrun+'/tasmin/*_'+srch+'*')
			
			if(var == 'tavg'):
				files = glob.glob('/mnt/ds-s3LOCA/'+model+'/daily/*'+era+'*_'+srch+'*')	
			
			ndays = [31,28,31,30,31,30,31,31,30,31,30,31]
			if(calendar.isleap(year)):
				ndays = [31,29,31,30,31,30,31,31,30,31,30,31]
			
			for k in range(len(mm)):	
				d1 = int(format(datetime(year,k+1,1), '%j'))-1
				d2 = int(format(datetime(year,k+1,ndays[k]), '%j'))-1
				
				#account for the short day in Dec 2099 for bcc-csm1-1 rcp85
				if(model == 'bcc-csm1-1' and era == 'rcp85' and yyyy == '2099'): d2 = 363
				
				cdfvar = var
				if(var == 'tavg'): cdfvar = 'avg'
				ofile = mm[k]+'_'+yyyy+'_daily_'+var+'_'+model+'_'+era+'.nc'
				
				#Check if file already exists
				if(enviro == 'S3'):
					ptf = '/mnt/ds-s3LOCA/'+model+'/daily_by_month/'+ofile
				if(enviro == 'local'):
					ptf = './daily_by_month/'+ofile
				fchk = os.path.exists(ptf)
				if(str(fchk) == 'False'):
					#print 'Needs processed: '+ofile
					tempfile = 'temp_'+era+'.nc'
					cmd = 'cp '+files[0]+' '+tempfile
					subprocess.call(cmd,shell=True)
					cmd = 'ncks -O -v '+cdfvar+' -d time,'+str(d1)+','+str(d2)+' '+tempfile+' '+ofile
					print cmd
					subprocess.call(cmd,shell=True)
					
					if not os.path.isdir('/mnt/ds-s3LOCA/'+model+'/daily_by_month'):
						cmd = 'mkdir /mnt/ds-s3LOCA/'+model+'/daily_by_month'
					subprocess.call(cmd, shell=True)
					cmd = 'cp '+ofile+' /mnt/ds-s3LOCA/'+model+'/daily_by_month/'+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'rm '+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'rm '+tempfile
					subprocess.call(cmd,shell=True)
					
					
				
