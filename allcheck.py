#!/work/anaconda2/bin/python

import os, sys, subprocess, glob, calendar
from datetime import datetime



if __name__ == '__main__':

	models = ['ACCESS1-0','ACCESS1-3','bcc-csm1-1','bcc-csm1-1-m','CanESM2','CCSM4',
	'CESM1-BGC','CESM1-CAM5','CMCC-CM','CMCC-CMS','CNRM-CM5','CSIRO-Mk3-6-0',
	'EC-EARTH','FGOALS-g2','GFDL-CM3','GFDL-ESM2G','GFDL-ESM2M','GISS-E2-H',
	'GISS-E2-R','HadGEM2-AO','HadGEM2-CC','HadGEM2-ES','inmcm4','IPSL-CM5A-LR',
	'IPSL-CM5A-MR','MIROC5','MIROC-ESM','MIROC-ESM-CHEM','MPI-ESM-LR','MPI-ESM-MR',
	'MRI-CGCM3','NorESM1-M']
	
	for i in range(len(models)):
		cmd = 'python check4errors.py '+models[i]+' rcp45 tavg S3'
		subprocess.call(cmd,shell=True)
		cmd = 'python check4errors.py '+models[i]+' rcp85 tavg S3'
		subprocess.call(cmd,shell=True)