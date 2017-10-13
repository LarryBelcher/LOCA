#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
import os, datetime, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap, addcyclic
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.font_manager as font_manager
from PIL import Image
from netCDF4 import Dataset
from PIL import ImageFont
from matplotlib.patches import Polygon as MplPolygon
import shapefile


def int2month(mmi):
	if(mmi == 0): mms = 'No Data'
	if(mmi == 1): mms = 'January'
	if(mmi == 2): mms = 'February'
	if(mmi == 3): mms = 'March'
	if(mmi == 4): mms = 'April'
	if(mmi == 5): mms = 'May'
	if(mmi == 6): mms = 'June'
	if(mmi == 7): mms = 'July'
	if(mmi == 8): mms = 'August'
	if(mmi == 9): mms = 'September' 
	if(mmi == 10): mms = 'October'
	if(mmi == 11): mms = 'November'
	if(mmi == 12): mms = 'December'	
	return mms


def gmtColormap(fileName):

      import colorsys
      import numpy as N
      try:
          f = open(fileName)
      except:
          print "file ",fileName, "not found"
          return None

      lines = f.readlines()
      f.close()

      x = []
      r = []
      g = []
      b = []
      colorModel = "RGB"
      for l in lines:
          ls = l.split()
          if l[0] == "#":
             if ls[-1] == "HSV":
                 colorModel = "HSV"
                 continue
             else:
                 continue
          if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
             pass
          else:
              x.append(float(ls[0]))
              r.append(float(ls[1]))
              g.append(float(ls[2]))
              b.append(float(ls[3]))
              xtemp = float(ls[4])
              rtemp = float(ls[5])
              gtemp = float(ls[6])
              btemp = float(ls[7])

      x.append(xtemp)
      r.append(rtemp)
      g.append(gtemp)
      b.append(btemp)

      nTable = len(r)
      x = N.array( x , N.float32)
      r = N.array( r , N.float32)
      g = N.array( g , N.float32)
      b = N.array( b , N.float32)
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "RGB":
          r = r/255.
          g = g/255.
          b = b/255.
      xNorm = (x - x[0])/(x[-1] - x[0])

      red = []
      blue = []
      green = []
      for i in range(len(x)):
          red.append([xNorm[i],r[i],r[i]])
          green.append([xNorm[i],g[i],g[i]])
          blue.append([xNorm[i],b[i],b[i]])
      colorDict = {"red":red, "green":green, "blue":blue}
      return (colorDict)


if __name__ == '__main__':

	var = sys.argv[1] #(expects tavg, tasmax, tasmin)

	mm = int(sys.argv[2]) #e.g., 1 through 12
	data_index = mm - 1
	if(mm == 0): data_index = 0
	mms = int2month(mm)
	
	dec = sys.argv[3]
	decEnd = int(dec)+9
	decEnd = str(decEnd)
	decrange = str(dec)+'-'+decEnd
	
	rcp = sys.argv[4] #(rcp45 or rcp85)
	
	imgsize = sys.argv[5]   #(expects 620, 1000, DIY, HD, or HDSD)


	if(rcp == 'rcp45' and imgsize == '620'): rcptext = 'Stabilized emissions \n (RCP 4.5)'
	if(rcp == 'rcp85' and imgsize == '620'): rcptext = 'High emissions \n (RCP 8.5)'
	
	if(rcp == 'rcp45' and imgsize != '620'): rcptext = 'Stabilized emissions (RCP 4.5)'
	if(rcp == 'rcp85' and imgsize != '620'): rcptext = 'High emissions (RCP 8.5)'
	
	ncvar = var
	if(var == 'tavg'): ncvar = 'avg'
	
	if(mm != 0):
		ncFile = '../Ensemble/'+mms[0:3]+'_'+dec+'-'+decEnd+'_'+var+'_ensemble_'+rcp+'.nc'
	if(mm == 0):
		decrange = ''
		ncFile = '../Ensemble/Jan_'+dec+'-'+decEnd+'_'+var+'_ensemble_'+rcp+'.nc'
	fh = Dataset(ncFile, mode='r')
	lons = fh.variables['lon'][:]
	lats = fh.variables['lat'][:]
	data = fh.variables[ncvar][0,:,:]
	fh.close()




	path = './Fonts/Trebuchet_MS.ttf'
	propr = font_manager.FontProperties(fname=path)
	path = './Fonts/Trebuchet_MS_Bold.ttf'
	propb = font_manager.FontProperties(fname=path)

	if(imgsize == '620'):
		figxsize = 8.62
		figysize = 5.56
		figdpi = 72
		lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
		logo_image = './noaa_logo_42.png'
		logo_x = 566
		logo_y = 4
		framestat = 'False'
		base_img = './CONUS_620_BaseLayer.png'
		line_img = './CONUS_620_stateLines.png'
		bgcol = '#F5F5F5'
		cmask = "./Custom_mask.png"

	if(imgsize == '1000'):
		figxsize = 13.89
		figysize = 8.89
		figdpi = 72
		lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
		logo_image = './noaa_logo_42.png'
		logo_x = 946
		logo_y = 4
		framestat = 'False'
		base_img = './CONUS_1000_BaseLayer.png'
		line_img = './CONUS_1000_stateLines.png'
		cmask = "./Custom_mask.png"
		bgcol = '#F5F5F5'

	if(imgsize == 'DIY'):
		figxsize = 13.655
		figysize = 8.745
		figdpi = 300
		lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
		logo_image = './noaa_logo.eps'
		logo_x = 946
		logo_y = 4
		framestat = 'False'
		base_img = './CONUS_DIY_BaseLayer.png'
		line_img = './CONUS_DIY_stateLines.png'
		cmask = "./Custom_mask.png"
		bgcol = '#F5F5F5'

	if(imgsize == 'HD'):
		figxsize = 21.33
		figysize = 10.25
		figdpi = 72
		#lllon, lllat, urlon, urlat = [-123.89399, 19.66787, -53.30945, 48.18950]
		lllon, lllat, urlon, urlat = [-126.95182, 19.66787, -52.88712, 46.33016]
		logo_image = './noaa_logo_100.png'
		logo_x = 1422
		logo_y = 34
		framestat = 'True'
		base_img = './CONUS_HD_BaseLayer.png'
		line_img = './CONUS_HD_stateLines.png'
		cmask = "./Custom_HD_mask.png"
		framestat = 'False'
		bgcol = '#F5F5F5'

	if(imgsize == 'HDSD'):
		figxsize = 16
		figysize = 9.75
		figdpi = 72
		lllon, lllat, urlon, urlat = [-120.8000, 19.5105, -57.9105, 48.9905]
		logo_image = './noaa_logo_100.png'
		logo_x = 1037
		logo_y = 35
		framestat = 'True'
		base_img = './CONUS_HDSD_BaseLayer.png'
		line_img = './CONUS_HDSD_stateLines.png'
		cmask = "./Custom_HDSD_mask.png"
		framestat = 'False'
		bgcol = '#F5F5F5'


	fig = plt.figure(figsize=(figxsize,figysize))
	# create an axes instance, leaving room for colorbar at bottom.
	ax1 = fig.add_axes([0.0,0.0,1.0,1.0], frameon=framestat)#, axisbg=bgcol)
	ax1.spines['left'].set_visible(False)
	ax1.spines['right'].set_visible(False)
	ax1.spines['bottom'].set_visible(False)
	ax1.spines['top'].set_visible(False)

	# Create Map and Projection Coordinates
	kwargs = {'epsg' : 5070,
	          'resolution' : 'i',
	          'llcrnrlon' : lllon,
	          'llcrnrlat' : lllat,
	          'urcrnrlon' : urlon,
	          'urcrnrlat' : urlat,
	          'lon_0' : -96.,
	          'lat_0' : 23.,
	          'lat_1' : 29.5,
	          'lat_2' : 45.5,
			  'area_thresh' : 15000,
			  'ax' : ax1,
			  'fix_aspect' : False
	}

	#Set up the Basemap
	m =Basemap(**kwargs)


	#Add the BaseLayer image 1st pass
	outline_im = Image.open(base_img)
	m.imshow(outline_im, origin='upper', aspect='auto')


	ny = data.shape[0]; nx = data.shape[1]
	#lons1, lats = m.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
	lons, lats = np.meshgrid(lons,lats)
	x, y = m(lons, lats) # compute map proj coordinates.


	#lons, lats = np.meshgrid(lons,lats)
	#xx, yy = m(lons, lats)

	
	cdict1 = gmtColormap('./CPT/temperature_10-110.cpt')
	cmap = LinearSegmentedColormap('this_cmap', cdict1)
	levs = np.asarray(xrange(202))*0.5+10.
	norm = colors.Normalize(levs[0], levs[-1])
	#data = np.nan_to_num(data)
	#data[np.isnan(data)] = 999.
	data[np.where((data >= 110.) & (data <= 9999.))] = 110.
	data[np.where((data <= 10.) & (data <= 9999.))] = 10.
	#data[np.where(data >= 999.)] = np.nan


	if(mm != 0):
		cdat = m.contourf(x, y, data, levs, ax=ax1, cmap=cmap, norm=norm, alpha=0.55)
		#call contourf again to eliminate lines (some magic I dug up form google, seems to work...)
		cdat1 = m.contourf(x, y, data, levs, ax=ax1, cmap=cmap, norm=norm, alpha=0.90)



	'''/Users/belcher/anaconda2/bin/python
	tmask = Image.open('testmask.png')
	m.imshow(tmask, origin='upper', alpha=1., zorder=10, aspect='auto', interpolation='nearest')
	
	tmask1 = Image.open('testmask1.png')
	m.imshow(tmask1, origin='upper', alpha=1., zorder=10, aspect='auto', interpolation='nearest')
	

	#Add the Line image
	#outline_im = Image.open(line_img)
	#m.imshow(outline_im, origin='upper', alpha=1.0, zorder=10, aspect='auto')

	
	world_shp_info = m.readshapefile('./Shapefiles/CNTR_2014_10M_SH/Data/CNTR_RG_10M_2014','world',drawbounds=False)

	ax = plt.gca()
	for shapedict,state in zip(m.world_info, m.world):
	    if shapedict['CNTR_ID'] not in ['CA', 'MX']: continue
	    poly = MplPolygon(state,facecolor='#e2e2e2',edgecolor='#e2e2e2',linestyle='solid',linewidth=0.001)
	    ax.add_patch(poly)
	'''
	
	omask_im = Image.open(cmask)
	m.imshow(omask_im, origin='upper', alpha=1., zorder=10, aspect='auto', interpolation='nearest')
	
	
	#Add the Line image
	outline_im = Image.open(line_img)
	m.imshow(outline_im, origin='upper', alpha=0.75, zorder=10, aspect='auto')


	#Add the NOAA logo (except for DIY)
	if(imgsize != 'DIY'):
		logo_im = Image.open(logo_image)
		height = logo_im.size[1]
		# We need a float array between 0-1, rather than
		# a uint8 array between 0-255 for the logo
		logo_im = np.array(logo_im).astype(np.float) / 255
		fig.figimage(logo_im, logo_x, logo_y, zorder=10)

	
	#Add the data citation
	lon, lat = lllon, lllat+3.6
	xpt, ypt = m(lon, lat)
	
	'''
	plt.text(xpt-30000, ypt, 'Prism Climate Group', fontproperties=propr, size=10, color='#8D8D8D')
	plt.text(xpt-30000, ypt-70000, 'Oregon State University', fontproperties=propr, size=10, color='#8D8D8D')
	plt.text(xpt-30000, ypt-140000, 'http://prism.oregonstate.edu', fontproperties=propr, size=10, color='#8D8D8D')
	plt.text(xpt-30000, ypt-210000, 'created 10 July 2012', fontproperties=propr, size=8.5, color='#8D8D8D')
	'''
	
	if(imgsize == 'HD' or imgsize =='HDSD'):
		if(var == 'tavg'):
			plt.text(xpt-30000, ypt-220000, 'Average temperature '+decrange, fontproperties=propr, size=15.7, color='#666666')
			plt.text(xpt-30000, ypt-300000, rcptext, fontproperties=propr, size=14.7, color='#666666')
		if(var == 'tasmax'):
			plt.text(xpt-30000, ypt-220000, 'Average maximum temperature '+decrange, fontproperties=propr, size=15.7, color='#666666')
			plt.text(xpt-30000, ypt-300000, rcptext, fontproperties=propr, size=14.7, color='#666666')
		if(var == 'tasmin'):
			plt.text(xpt-30000, ypt-220000, 'Average minimum temperature '+decrange, fontproperties=propr, size=15.7, color='#666666')
			plt.text(xpt-30000, ypt-300000, rcptext, fontproperties=propr, size=14.7, color='#666666')




	outpng = "temporary_map.png"

	if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
		plt.savefig(outpng,dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.00)

	if(imgsize == 'HD' or imgsize =='HDSD'):
		plt.savefig(outpng, dpi=figdpi, orientation='landscape')#, bbox_inches='tight', pad_inches=0.01)


