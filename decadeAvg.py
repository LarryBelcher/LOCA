#!/work/anaconda2/bin/python

'''
	Example Usage:
	decadeAvg.py "model" "rcp" "var"
	
	where,
	model 		=	Any of the GCM's
	rcp			=	either rcp45 or rcp85 (the two preferred carbon pathways)
	var			= 	either tavg, tasmax, pr tasmin
	
'''

import os, sys, subprocess, glob, calendar
from datetime import datetime



if __name__ == '__main__':

	model = sys.argv[1]
	era = sys.argv[2]
	var = sys.argv[3]

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
	sy = ['2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090']
	
	for i in range(len(mm)):
		for j in range(len(sy)):
			
			if(var == 'tasmax'):
				ofile = mm[i]+'_'+sy[j]+'-'+str(int(sy[j])+9)+'_'+var+'_'+model+'_'+era+'.nc'
				fullpath = '/mnt/ds-s3LOCA/'+model+'/decade/'+ofile
				if not os.path.isfile(fullpath):
					files = glob.glob('/mnt/ds-s3LOCA/'+model+'/daily_by_month/'+mm[i]+'*'+sy[j][:3]+'*tasmax*'+era+'.nc')
					cmd = 'ncra '+" ".join(files)+' tmp.nc'
					subprocess.call(cmd,shell=True)
					cmd = 'cdo expr,tasmax=tasmax*1.8-459.67 tmp.nc '+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'rm tmp.nc'
					subprocess.call(cmd,shell=True)
					cmd = 'ncatted -a units,tasmax,o,c,degrees_F '+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'ncatted -a long_name,tasmax,o,c,maximum_temperature '+ofile
					subprocess.call(cmd,shell=True)
					if not os.path.isdir('/mnt/ds-s3LOCA/'+model+'/decade'):
						cmd = 'mkdir /mnt/ds-s3LOCA/'+model+'/decade'
						subprocess.call(cmd,shell=True)
					cmd = 'cp '+ofile+' /mnt/ds-s3LOCA/'+model+'/decade/'+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'rm '+ofile
					subprocess.call(cmd,shell=True)
			
			if(var == 'tasmin'):
				ofile = mm[i]+'_'+sy[j]+'-'+str(int(sy[j])+9)+'_'+var+'_'+model+'_'+era+'.nc'
				fullpath = '/mnt/ds-s3LOCA/'+model+'/decade/'+ofile
				if not os.path.isfile(fullpath):
					files = glob.glob('/mnt/ds-s3LOCA/'+model+'/daily_by_month/'+mm[i]+'*'+sy[j][:3]+'*tasmin*'+era+'.nc')
					cmd = 'ncra '+" ".join(files)+' tmp.nc'
					subprocess.call(cmd,shell=True)
					cmd = 'cdo expr,tasmin=tasmin*1.8-459.67 tmp.nc '+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'rm tmp.nc'
					subprocess.call(cmd,shell=True)
					cmd = 'ncatted -a units,tasmin,o,c,degrees_F '+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'ncatted -a long_name,tasmin,o,c,minimum_temperature '+ofile
					subprocess.call(cmd,shell=True)
					if not os.path.isdir('/mnt/ds-s3LOCA/'+model+'/decade'):
						cmd = 'mkdir /mnt/ds-s3LOCA/'+model+'/decade'
						subprocess.call(cmd,shell=True)
					cmd = 'cp '+ofile+' /mnt/ds-s3LOCA/'+model+'/decade/'+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'rm '+ofile
					subprocess.call(cmd,shell=True)
			
			if(var == 'tavg'):
				ofile = mm[i]+'_'+sy[j]+'-'+str(int(sy[j])+9)+'_'+var+'_'+model+'_'+era+'.nc'
				fullpath = '/mnt/ds-s3LOCA/'+model+'/decade/'+ofile
				if not os.path.isfile(fullpath):
					files = glob.glob('/mnt/ds-s3LOCA/'+model+'/daily_by_month/'+mm[i]+'*'+sy[j][:3]+'*tavg*'+era+'.nc')
					cmd = 'ncra '+" ".join(files)+' '+ofile
					subprocess.call(cmd,shell=True)
					if not os.path.isdir('/mnt/ds-s3LOCA/'+model+'/decade'):
						cmd = 'mkdir /mnt/ds-s3LOCA/'+model+'/decade'
						subprocess.call(cmd,shell=True)
					cmd = 'cp '+ofile+' /mnt/ds-s3LOCA/'+model+'/decade/'+ofile
					subprocess.call(cmd,shell=True)
					cmd = 'rm '+ofile
					subprocess.call(cmd,shell=True)
			
			