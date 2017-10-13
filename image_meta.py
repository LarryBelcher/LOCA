#!/usr/bin/python
'''
        Program: image_meta.py
        Abstract: A simple python script to print out file creation times
        Usage: image_meta.py "Path to files"
                where "path to files" is an exact file system path to the files 
                which information will be printed  

'''
import os.path, time, glob, sys

fpath = sys.argv[1]+"*.png"
files = glob.glob(fpath)

f = open("image_metadata.txt","w")
for file in sorted(files):
        fname = file.split('/')[len(file.split('/'))-1]
        f.write(fname+" created: %s" % time.ctime(os.path.getmtime(file))+"\n")
        
f.close()
