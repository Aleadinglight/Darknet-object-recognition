# -*- coding: utf-8 -*-

import os
from os import walk, getcwd
from PIL import Image

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
#--------------------------------------------------------------------------------- 

# Fill in with all your objects
classes = ["thumb","helmet"]   
# Path to the current object we are going to modify
path = "./"
outpath = "out/"
# Input here the image path
my_img_path = "img/" 





# Main process
for cls in classes:
	cls_id = classes.index(cls)
	wd = getcwd()
	
	# This one will list the names of your .txt here so you can pass it to training instruction later

	# Get input text file list
	txt_name_list = []
	# append all the filenames to txt_name_list[]
	mypath=path+cls+"/"
	filenames = os.listdir(mypath)
	txt_name_list.extend(filenames)
	print("txt name list: ",txt_name_list)
	for txt_name in txt_name_list:
	    txt_path = mypath + txt_name
	    print("Input: " + txt_path)
	    txt_file = open(txt_path, "r")
	    lines = txt_file.read().split('\n')   #for ubuntu, use "\r\n" instead of "\n"
	    
	#	open output file in append format
	# 	because one file contain many objects
	    txt_outpath = outpath + txt_name
	    print("Output: " + txt_outpath)
	    txt_outfile = open(txt_outpath, "a")
	    
	#	Convert to YOLOv2 format
	    count = 0
	    print lines
	    for line in lines:
	        #print('lenth of line is: ')
	        #print(len(line))
	        #print('\n')
	        if(len(line.split(' ')) >= 2):
	            count = count + 1
	            print(line)
	            input = line.split(' ')
	            print("input",input)
	            xleft = input[0]
	            xright = input[2]
	            ybot = input[1]
	            ytop = input[3]
	            print my_img_path
	            print os.path.splitext(txt_name)[0]
	            img_path = str('%s%s.JPEG'%(my_img_path,os.path.splitext(txt_name)[0]))
	           
	            print "Img path: ",img_path
	            im=Image.open(img_path)
	            w= int(im.size[0])
	            h= int(im.size[1])
	            #w = int(xmax) - int(xmin)
	            #h = int(ymax) - int(ymin)
	            # print(xmin)
	            print(w, h)
	            b = (float(xleft), float(xright), float(ybot), float(ytop))
	            bb = convert((w,h), b)
	            print(bb)
	# 			<object id> <data...>...	
	            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


imgs = os.listdir(my_img_path)
print "Save all pictures name to: ",my_img_path,"name_list.txt"
list_file = open('%s/name_list.txt'%wd, 'w')
for img in imgs:
	list_file.write('%s%s.JPEG\n'%(my_img_path,os.path.splitext(img)[0]))                
list_file.close()       
