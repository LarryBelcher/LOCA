#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os, datetime, sys
import numpy as np
#import _imaging


def int2month(mmi):
	if(mmi == '0'): mms = 'No Data'
	if(mmi == '1'): mms = 'January'
	if(mmi == '2'): mms = 'February'
	if(mmi == '3'): mms = 'March'
	if(mmi == '4'): mms = 'April'
	if(mmi == '5'): mms = 'May'
	if(mmi == '6'): mms = 'June'
	if(mmi == '7'): mms = 'July'
	if(mmi == '8'): mms = 'August'
	if(mmi == '9'): mms = 'September'
	if(mmi == '10'): mms = 'October'
	if(mmi == '11'): mms = 'November'
	if(mmi == '12'): mms = 'December'	
	return mms


if __name__ == '__main__':


	var = sys.argv[1] #(expects tavg, tasmax, tasmin)

	mm = sys.argv[2] #e.g., 1 through 12
	mms = int2month(mm)
	if(int(mm) < 10): mmm = '0'+mm
	if(int(mm) >= 10): mmm = mm
	
	dec = sys.argv[3] #(2020, 2030, 2040...)
	decEnd = int(dec)+9
	decEnd = str(decEnd)
	
	rcp = sys.argv[4]
	
	imgsize = sys.argv[5]   #(expects 620, 1000, DIY, HD, or HDSD)




	figdpi = 72

	cmd = "python ./LocaMap.py "+var+" "+mm+" "+dec+" "+rcp+" "+imgsize
	os.system(cmd)

	cmd = "python ./LocaColorbar.py "+var+" "+mm+" "+dec+" "+rcp+" "+imgsize
	
	os.system(cmd)
	if(var == "tavg"):
		if(mms == 'No Data'): 
			mms = 'No-Data'
			dec = '0000'
			decEnd = '0000'
	inamepre = "averagetemp-"+mms+"-"+dec+"-"+decEnd+"-LOCA-"+rcp+"--"
	if(var == "tasmax"):
		if(mms == 'No Data'): 
			mms = 'No-Data'
			dec = '0000'
			decEnd = '0000'
		inamepre = "averagemaxtemp-"+mms+"-"+dec+"-"+decEnd+"-LOCA-"+rcp+"--"
	if(var == "tasmin"):
		if(mms == 'No Data'): 
			if(mms == 'No Data'): 
				mms = 'No-Data'
				dec = '0000'
				decEnd = '0000'
		inamepre = "averagemintemp-"+mms+"-"+dec+"-"+decEnd+"-LOCA-"+rcp+"--"

	decrange = str(dec)+'-'+decEnd
		
	if not os.path.isdir('./Images'):
		cmd = 'mkdir ./Images'
		os.system(cmd)
	if not os.path.isdir('./Images/'+var):
		cmd = 'mkdir ./Images/'+var
		os.system(cmd)
	if not os.path.isdir('./Images/'+var+'/'+imgsize.lower()):
		cmd = 'mkdir ./Images/'+var+'/'+imgsize.lower()
		os.system(cmd)


	if(imgsize == '620' or imgsize == '1000'):
		im1 = Image.open("temporary_map.png")
		im2 = Image.open("temporary_cbar.png")
		im3 = Image.new('RGBA', size = (im1.size[0], im1.size[1]+im2.size[1]))
		im3.paste(im2, (0,im1.size[1]))
		im3.paste(im1, (0,0))
		img_path = './Images/'+var+'/'+imgsize.lower()+'/'
		imgw = str(im3.size[0])
		imgh = str(im3.size[1])
		img_name = inamepre+imgw+'x'+imgh+'--0000-'+mmm+'-00.png'
		pngfile = img_path+img_name
		print "Saving "+pngfile
		im3.save(pngfile)


	if(imgsize == 'DIY'):
		im1 = "./temporary_map.png"
		imgs = Image.open(im1)
		imgw = str(imgs.size[0])
		imgh = str(imgs.size[1])
		img_path = './Images/'+var+'/'+imgsize.lower()+'/'
		img_name = inamepre+imgw+'x'+imgh+'--0000-'+mmm+'-00.png'
		cmd = 'mv '+im1+' '+img_name
		os.system(cmd)
		im2 = "./temporary_cbar.eps"
		cbar_name = inamepre+imgw+'x'+imgh+'--0000-'+mmm+'-00_colorbar.eps'
		cmd = 'mv '+im2+' '+cbar_name
		os.system(cmd)	
		cmd1 = 'zip '+inamepre+imgw+'x'+imgh+'--0000-'+mmm+'-00.zip '+img_name+' '+cbar_name+' noaa_logo.eps '
		os.system(cmd1)
		cmd2 = 'mv '+inamepre+imgw+'x'+imgh+'--0000-'+mmm+'-00.zip '+img_path
		os.system(cmd2)
		cmd3 = 'rm '+img_name+' '+cbar_name
		os.system(cmd3)
	
	
	if(imgsize == 'HD'):
		hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
		imgw = '1920'
		imgh = '1080'
	
		im1 = Image.open("temporary_map.png")
		bbox = (1,1,1535,738)
		im1 = im1.crop(bbox)
		osize = im1.size
		new_size = (osize[0]+2,osize[1]+2)
		im1new = Image.new("RGB", new_size)
		im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
		hdim.paste(im1new, (192,108))
	
		draw = ImageDraw.Draw(hdim)
		fntpath = './Fonts/Trebuchet_MS.ttf'
		fnt1 = ImageFont.truetype(fntpath, 18)
		if(mm == '0'): xpos = 1632
		if(mm == '1'): xpos = 1630
		if(mm == '2'): xpos = 1627
		if(mm == '3'): xpos = 1639
		if(mm == '4'): xpos = 1644
		if(mm == '5'): xpos = 1648
		if(mm == '6'): xpos = 1642
		if(mm == '7'): xpos = 1646
		if(mm == '8'): xpos = 1638
		if(mm == '9'): xpos = 1619	
		if(mm == '10'): xpos = 1633
		if(mm == '11' or mm == '12'): xpos = 1623	
		if(mms == 'No-Data'): mms = 'No Data'
		draw.text((xpos,815), mms, (0,0,0), font=fnt1)
		#xpos = 1662 - ((len(mms)*8)-9)/2
		#draw.text((xpos,815), mms, (0,0,0), font=fnt1)

	
		#Add the colorbar
		cbar_orig = Image.open('temporary_cbar.png')
		bbox = (1,1,972,43)
		cbar_orig = cbar_orig.crop(bbox)
		old_size = cbar_orig.size
		new_size = (old_size[0]+2,old_size[1]+2)
		cbar_im = Image.new("RGB", new_size)
		cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
	                      (new_size[1]-old_size[1])/2))
		hdim.paste(cbar_im, (474,866))

		
		fnt4 = ImageFont.truetype(fntpath, 47)
		text2 = "cool"
		draw.text((515,905), text2, (0,0,0), font=fnt4)
		text3 = "warm"
		draw.text((1290,905), text3, (0,0,0), font=fnt4)
		#text3 = "Normals"
		#draw.text((870,915), text3, (0,0,0), font=fnt4)
		
		draw.polygon([(500,946), (485,936), (500,926)], fill="black", outline="black")
		draw.polygon([(1420,946), (1435,936), (1420,926)], fill="black", outline="black")
	
	

	
		img_path = './Images/'+var+'/'+imgsize.lower()+'/'
		img_name = inamepre+imgw+'x'+imgh+'hd--0000-'+mmm+'-00.png'
		pngfile = img_path+img_name
		print "Saving "+pngfile
		hdim.save(pngfile)


	if(imgsize == 'HDSD'):
		hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
		imgw = '1920'
		imgh = '1080'
	
		im1 = Image.open("temporary_map.png")
		bbox = (1,1,1152,702)
		im1 = im1.crop(bbox)
		osize = im1.size
		new_size = (osize[0]+2,osize[1]+2)
		im1new = Image.new("RGB", new_size)
		im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
		hdim.paste(im1new, (384,108))
	
		draw = ImageDraw.Draw(hdim)
		fntpath = './Fonts/Trebuchet_MS.ttf'
		#fnt1 = ImageFont.truetype(fntpath, 18)
		#xpos = 1470 - ((len(mms)*8)-9)/2
	
		fnt1 = ImageFont.truetype(fntpath, 18)
		if(mm == '0'): xpos = 1440
		if(mm == '1'): xpos = 1440
		if(mm == '2'): xpos = 1436
		if(mm == '3'): xpos = 1448
		if(mm == '4'): xpos = 1453
		if(mm == '5'): xpos = 1457
		if(mm == '6'): xpos = 1453
		if(mm == '7'): xpos = 1455
		if(mm == '8'): xpos = 1446
		if(mm == '9'): xpos = 1428
		if(mm == '10'): xpos = 1440
		if(mm == '11' or mm == '12'): xpos = 1432
		if(mms == 'No-Data'): mms = 'No Data'
		draw.text((xpos,781), mms, (0,0,0), font=fnt1)
	
	
		#Add the colorbar
		cbar_orig = Image.open('temporary_cbar.png')
		bbox = (1,1,972,43)
		cbar_orig = cbar_orig.crop(bbox)
		old_size = cbar_orig.size
		new_size = (old_size[0]+2,old_size[1]+2)
		cbar_im = Image.new("RGB", new_size)
		cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
	                      (new_size[1]-old_size[1])/2))
		hdim.paste(cbar_im, (474,830))
			
		
		fnt4 = ImageFont.truetype(fntpath, 47)
		text2 = "cool"
		draw.text((515,870), text2, (0,0,0), font=fnt4)
		text3 = "warm"
		draw.text((1290,870), text3, (0,0,0), font=fnt4)
		#text4 = "Normals"
		#draw.text((865,875), text4, (0,0,0), font=fnt4)
	
		draw.polygon([(500,911), (485,901), (500,891)], fill="black", outline="black")
		draw.polygon([(1420,911), (1435,901), (1420,891)], fill="black", outline="black")
	

	
		img_path = './Images/'+var+'/'+imgsize.lower()+'/'
		img_name = inamepre+imgw+'x'+imgh+'hdsd--0000-'+mmm+'-00.png'
		pngfile = img_path+img_name
		print "Saving "+pngfile
		hdim.save(pngfile)
		
		
		
		