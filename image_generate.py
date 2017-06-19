import cv2
import numpy as np
import glob
from lib.image_generator import *
from lib.xmlgenerator import *
from IPython.core.debugger import Tracer; keyboard = Tracer()

print("loading image generator...")
input_width = 480
input_height = 480
item_path = "./items/"
#background_path = "./backgrounds/"
background_path = "./background_bin/"
Generate_folder = "./"
seriesname = "Bin_Generated_Data_"
generator = ImageGenerator(item_path, background_path)

#sets = 5
sets = 100
n_samples = 100
n_items=10

delta_hue=0.03
delta_sat_scale=0.2
delta_val_scale=0.2
min_item_scale=1.0
max_item_scale=1.2
rand_angle=90
minimum_crop=0.85


def restrict_value_in_image(anno,width,height):
    xmin = max(anno[0],0)
    xmax = min(anno[1],width)
    ymin = max(anno[2],0)
    ymax = min(anno[3],height)
    return [xmin,xmax,ymin,ymax]


def get_annotation_value(box):
    #classname,box_x,box_y,box_w,box_hs
    x = box[1]
    y = box[2]
    w = box[3]
    h = box[4]
    xmin = int(x-w/2)
    xmax = int((x + w/2))
    ymin = int(y-h/2)
    ymax = int((y + h/2))
    return [xmin,xmax,ymin,ymax]

def get_classname(filename):
    classname = filename.split("-")[0]
    return classname

number = 1
for set in range(sets):
    # generate random sample
    x, t = generator.generate_samples(
        n_samples=n_samples,
        n_items=n_items,
        crop_width=input_width,
        crop_height=input_height,
        min_item_scale=min_item_scale,
        max_item_scale=max_item_scale,
        rand_angle=rand_angle,
        minimum_crop=minimum_crop,
        delta_hue=delta_hue,
        delta_sat_scale=delta_sat_scale,
        delta_val_scale=delta_val_scale
    )
    for i, image in enumerate(x):
        image = np.transpose(image, (1, 2, 0)).copy()

        dataname=seriesname+"{}".format(number)
        imagename = dataname + ".png"
        XMLfolder = Generate_folder + "Annotation/"
        XMLpath = XMLfolder+dataname+".xml"
        if not os.path.isdir(XMLfolder):
            os.makedirs(XMLfolder)
        prepareXML(XMLpath,imagename,input_width,input_height)
        width, height, _ = image.shape
        for truth_box in t[i]:
            box_x, box_y, box_w, box_h = truth_box['x']*width, truth_box['y']*height, truth_box['w']*width, truth_box['h']*height
            classname = get_classname(generator.labels[truth_box['label']])
            box = [classname,box_x,box_y,box_w,box_h]
            anno = get_annotation_value(box)
            anno = restrict_value_in_image(anno,input_width,input_height)
            writeXML(XMLpath,box[0],anno)
            #image = cv2.rectangle(image.copy(), (int(box_x-box_w/2), int(box_y-box_h/2)), (int(box_x+box_w/2), int(box_y+box_h/2)), (0, 0, 255), 3)
            #image = cv2.rectangle(image.copy(),(anno[0],anno[2]),(anno[1],anno[3]) ,(0, 0, 255), 3)
        FinishXML(XMLpath)
        #print(t[i])
        image=(image*255).astype('uint8')
        Imagefolder = Generate_folder+"Images/"
        Imagepath = Imagefolder + dataname+".png"
        if not os.path.isdir(Imagefolder):
            os.makedirs(Imagefolder)
        cv2.imwrite(Imagepath,image*255)
        number = number+1
    print ("Set "+ str(set+1) + " Done.")
print ("Generate Finished.")

