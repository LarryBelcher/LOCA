#!/work/anaconda2/bin/python

'''
	Example Usage:
	decadeEnsemble50.py "rcp" "var"
	
	where,
	rcp			=	either rcp45 or rcp85 (the two preferred carbon pathways)
	var			= 	either tavg, tasmax, pr tasmin
	
'''

import os, sys, subprocess, glob, calendar
from datetime import datetime



if __name__ == '__main__':


	era = sys.argv[1]
	var = sys.argv[2]

	
	
	mm = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	sy = ['2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090']
	

	
	for i in range(len(mm)):
		for j in range(len(sy)):
			
			if(var == 'tasmax'):
				ofile = mm[i]+'_'+sy[j]+'-'+str(int(sy[j])+9)+'_'+var+'_ensemble_'+era+'.nc'
				fullpath = '/mnt/work/LOCA/Ensemble/'+ofile
				if not os.path.isfile(fullpath):
					files = glob.glob('/mnt/ds-s3LOCA/*/decade/'+mm[i]+'*'+sy[j][:3]+'*tasmax*'+era+'.nc')
					cmd = 'cdo enspctl,50 '+" ".join(files)+' '+ofile
					subprocess.call(cmd,shell=True)
			
			if(var == 'tasmin'):
				ofile = mm[i]+'_'+sy[j]+'-'+str(int(sy[j])+9)+'_'+var+'_ensemble_'+era+'.nc'
				fullpath = '/mnt/work/LOCA/Ensemble/'+ofile
				if not os.path.isfile(fullpath):
					files = glob.glob('/mnt/ds-s3LOCA/*/decade/'+mm[i]+'*'+sy[j][:3]+'*tasmin*'+era+'.nc')
					cmd = 'cdo enspctl,50 '+" ".join(files)+' '+ofile
					subprocess.call(cmd,shell=True)
			
			if(var == 'tavg'):
				ofile = mm[i]+'_'+sy[j]+'-'+str(int(sy[j])+9)+'_'+var+'_ensemble_'+era+'.nc'
				fullpath = '/mnt/work/LOCA/Ensemble/'+ofile
				if not os.path.isfile(fullpath):
					files = glob.glob('/mnt/ds-s3LOCA/*/decade/'+mm[i]+'*'+sy[j][:3]+'*tavg*'+era+'.nc')
					cmd = 'cdo enspctl,50 '+" ".join(files)+' '+ofile
					subprocess.call(cmd,shell=True)