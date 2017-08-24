import cv2
import os,sys
import re
import time
import json
import subprocess
from pprint import pprint
from IPython.terminal.debugger import set_trace as keyboard

def remove_background(imgpath_list,outputfolder):
	remove_background_img_list = []
	for imgpath in imgpath_list:
		output_filename = os.path.splitext(imgpath)[0].split("/")[-1]
		outputpath = os.path.join(outputfolder,output_filename+".png")
		cmd = ["/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/BackgroundRemoverBBoxExtractor/BackgroundRemoverBBoxExtractor",imgpath,outputpath,"8 10 50 0.99"]
		subprocess.call(cmd)
		remove_background_img_list.append(outputpath)
	return remove_background_img_list

def readjson_dimension(json_file):
	with open(json_file) as data_file:
		data = json.load(data_file)
	pprint(data)
	classname = data["name"]
	dimensions = data["dimensions"]
	return classname,dimensions


def start_resize_and_rename_cpp(imgpath_list,dimension,outputfolder,classname):
	print("Doing Resizing to "+str(classname)+"...")
	i = 1
	for imgpath in imgpath_list:
		dimension = [str(dimension[0]),str(dimension[1]),str(dimension[2])]
		filename = classname+"-"+str(i)+".png"
		filepath = os.path.join(outputfolder,filename)
		cmd = ["/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/ImageResizeWithRealDimension/ImageResizeWithRealDimension",imgpath,filepath,dimension[0],dimension[1],dimension[2]]
		subprocess.call(cmd)
		i += 1
	print("Done")


if __name__ == "__main__":
	argv = sys.argv
	if len(argv) != 4:
		print("Resize_image.py [Imgfolder_in] [Nobackground_Images] [Imgfolder_out]")
		exit()

	Imgfolder_in = argv[1]
	Nobackground_Images_out = argv[2]
	Imgfolder_out = argv[3]

	timestart = time.time()
	if Imgfolder_in[-1] != "/":
		Imgfolder_in=Imgfolder_in+"/"

	if Imgfolder_out[-1] != "/":
		Imgfolder_out=Imgfolder_out+"/"

	if Nobackground_Images_out[-1] != "/":
		Nobackground_Images_out=Nobackground_Images_out+"/"

	if os.path.isdir(Imgfolder_out) == False:
		os.makedirs(Imgfolder_out)

	if os.path.isdir(Nobackground_Images_out) == False:
		os.makedirs(Nobackground_Images_out)

	for element in os.listdir(Imgfolder_in):
		if os.path.isdir(os.path.join(Imgfolder_in,element)):
			#find jsonfile
			jsonfile_flag = False
			img_list = []
			element_realpath=os.path.join(Imgfolder_in,element)
			for file in os.listdir(element_realpath):
				if file.endswith(".json"):
					#classname=os.path.splitext(file)[0].split("/")[-1]
					jsonfile=os.path.join(element_realpath,file)
					classname,dimensions = readjson_dimension(jsonfile)
					jsonfile_flag = True
				if file.endswith(".png"):
					img_path = os.path.join(element_realpath,file)
					img_list.append(img_path)
			#print img_list
			nobackimage_list = remove_background(img_list,Nobackground_Images_out)
			start_resize_and_rename_cpp(nobackimage_list,dimensions,Imgfolder_out,classname)

	print "Time cost: " + str(time.time()-timestart)
