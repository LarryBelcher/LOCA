#!/work/anaconda2/bin/python



import os, datetime, sys, subprocess, glob



if __name__ == '__main__':

	model = sys.argv[1]
	era = ['historical', 'rcp45', 'rcp85']
	

	for i in range(len(era)):
		
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
		if(model == 'EC-EARTH' and era[i] == 'rcp45'): mrun = 'r8i1p1'
		if(model == 'EC-EARTH' and era[i] == 'rcp85'): mrun = 'r2i1p1'
		if(model == 'FGOALS-g2'): mrun = 'r1i1p1'
		if(model == 'GFDL-CM3'): mrun = 'r1i1p1'
		if(model == 'GFDL-ESM2G'): mrun = 'r1i1p1'
		if(model == 'GFDL-ESM2M'): mrun = 'r1i1p1'
		if(model == 'GISS-E2-H' and era[i] == 'historical'): mrun = 'r6i1p1'
		if(model == 'GISS-E2-H' and era[i] == 'rcp45'): mrun = 'r6i1p3'
		if(model == 'GISS-E2-H' and era[i] == 'rcp85'): mrun = 'r2i1p1'
		if(model == 'GISS-E2-R' and era[i] == 'historical' or era[i] == 'rcp45'): mrun = 'r6i1p1'
		if(model == 'GISS-E2-R' and era[i] == 'rcp85'): mrun = 'r2i1p1'				
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
		
		
		tasmaxfiles = glob.glob('/mnt/s3-LOCA/'+model+'/16th/'+era[i]+'/'+mrun+'/tasmax/*')
		tasminfiles = glob.glob('/mnt/s3-LOCA/'+model+'/16th/'+era[i]+'/'+mrun+'/tasmin/*')
	
	
		for j in range(len(tasmaxfiles)):
			fchk1 = tasmaxfiles[j].split(model)[2]
			fchk2 = tasminfiles[j].split(model)[2]
			if(fchk1 != fchk2): print '***Problem, file mis-match'
			
			#Now check if the tavg file has already been processed
			tfile = glob.glob('/mnt/ds-s3LOCA/'+model+'/daily/*'+fchk1)
			
			if(fchk1 == fchk2 and len(tfile) == 0):
				
				mergedofile = 'tmerged_day_'+model+fchk1
				print 'Working on '+mergedofile
				
				cmd = 'cdo merge '+tasmaxfiles[j]+' '+tasminfiles[j]+' '+mergedofile
				subprocess.call(cmd,shell=True)
				
				
				tavgfile = 'tavg_day_'+model+fchk1
				cmd = "cdo expr,'avg=(((tasmax+tasmin)/2.)*1.8)-459.67' "+mergedofile+' '+tavgfile
				subprocess.call(cmd,shell=True)
				
				
				cmd = 'ncatted -a long_name,avg,o,c,average_temperature '+tavgfile
				subprocess.call(cmd,shell=True)
				
				
				cmd = 'ncatted -a units,avg,o,c,degrees_F '+tavgfile
				subprocess.call(cmd,shell=True)
				
				
				cmd = 'rm '+mergedofile
				subprocess.call(cmd,shell=True)
				
				
				cmd = 'cp '+tavgfile+' /mnt/ds-s3LOCA/'+model+'/daily/'+tavgfile
				subprocess.call(cmd,shell=True)
				
				cmd = 'rm '+tavgfile
				subprocess.call(cmd,shell=True)			


