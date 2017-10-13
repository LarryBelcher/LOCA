#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
import os, datetime, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.font_manager as font_manager
from PIL import Image
from netCDF4 import Dataset

def int2month(mmi):
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

var = sys.argv[1]

mm = int(sys.argv[2]) #e.g., 1 through 12
data_index = mm - 1
mms = int2month(mm)


imgsize = sys.argv[3]   #(expects 620, 1000, DIY, HD, or HDSD)

ncFile = '../netcdf_data/normals/PRISM_'+var+'_30yr_normal_4kmM2_1981-2010_Jan-Dec.nc'
fh = Dataset(ncFile, mode='r')
lons = fh.variables['lon'][:]
lats = fh.variables['lat'][:]
data = fh.variables[var][data_index,:,:]
fh.close()


'''
# Read Data
f = np.load('./Data/allsevere.npz')
lons = f['lons']
lats = f['lats']
probs = f['probs']
del f
'''



path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)

if(imgsize == '620'):
	figxsize = 8.62
	figysize = 5.56
	figdpi = 72
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	#lllon,lllat,urlon,urlat = [lons.min(),lats.min(),lons.max(),lats.max()]
	logo_image = './noaa_logo_42.png'
	logo_x = 566
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_620_BaseLayer.png'
	line_img = './CONUS_620_stateLines.png'
	bgcol = '#F5F5F5'

if(imgsize == '1000'):
	figxsize = 13.89
	figysize = 8.89
	figdpi = 72
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	lllon, lllat, urlon, urlat = [-119.8939, 21.6578, -62.3194, 49.1899]
	logo_image = './noaa_logo_42.png'
	logo_x = 946
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_1000_BaseLayer.png'
	line_img = './CONUS_1000_stateLines.png'
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
	bgcol = '#F5F5F5'

if(imgsize == 'HD'):
	figxsize = 21.33
	figysize = 10.25
	figdpi = 72
	lllon, lllat, urlon, urlat = [-123.89399, 19.66787, -53.30945, 48.18950]
	logo_image = './noaa_logo_100.png'
	logo_x = 1426
	logo_y = 29
	framestat = 'True'
	base_img = './CONUS_HD_BaseLayer.png'
	line_img = './CONUS_HD_stateLines.png'
	framestat = 'False'
	bgcol = '#F5F5F5'

if(imgsize == 'HDSD'):
	figxsize = 16
	figysize = 9.75
	figdpi = 72
	lllon, lllat, urlon, urlat = [-120.8000, 19.5105, -57.9105, 48.9905]
	logo_image = './noaa_logo_100.png'
	logo_x = 1042
	logo_y = 29
	framestat = 'True'
	base_img = './CONUS_HDSD_BaseLayer.png'
	line_img = './CONUS_HDSD_stateLines.png'
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



lons, lats = np.meshgrid(lons,lats)
xx, yy = m(lons, lats)

if(var == 'ppt'):
	cdict1 = gmtColormap('./CPT/precipitation_0-8.cpt')
	cmap = LinearSegmentedColormap('this_cmap', cdict1)
	levs = [0,220] #np.asarray(xrange(81))*0.1
	norm = colors.Normalize(levs[0], levs[-1])
	data = np.nan_to_num(data)
	data[np.where(data > 0.)]=220
	data[np.where(data == 0.)]=np.nan
	
cmap = plt.cm.binary

cdat1 = m.contourf(xx, yy, data, levs, ax=ax1, cmap=cmap)


outpng = "temporary_map.png"

if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	plt.savefig(outpng,dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.00)

if(imgsize == 'HD' or imgsize =='HDSD'):
	plt.savefig(outpng, dpi=figdpi, orientation='landscape')#, bbox_inches='tight', pad_inches=0.01)


