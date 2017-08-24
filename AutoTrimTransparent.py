import cv2
import sys,os
from IPython.terminal.debugger import set_trace as keyboard

def isColEmpty(img,col):
    if img[col,:,3].sum() == 0:
        return True
    else:
        return False

def isRowEmpty(img,row):
    if img[:,row,3].sum() == 0:
        return True
    else:
        return False

def FindBoundaryAndCrop(img):
    width,height, channel = img.shape
    if channel != 4:
        print("The Image should be with alpha value! Use RGBA!")
        exit()
    minX = 0;
    minY = 0;
    maxX = width-1;
    #keyboard()
    maxY = height-1;
    while(minY<height and isRowEmpty(img,minY)):minY+=1
    while(maxY<height and isRowEmpty(img,maxY)):maxY-=1
    while(minX<width and isColEmpty(img,minX)):minX+=1
    while(maxX<width and isColEmpty(img,maxX)):maxX-=1
    print([minX,maxX,minY,maxY])
    img_crop = img[minX:maxX,minY:maxY]
    return img_crop

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 3:
        print("AutoTrimTransparent.py [Imgfolder_in] [Imgfolder_out]")
        exit()

    Imgfolder_in = argv[1]
    Imgfolder_out = argv[2]

    if Imgfolder_in[-1] != "/":
        Imgfolder_in=Imgfolder_in+"/"

    if Imgfolder_out[-1] != "/":
        Imgfolder_out=Imgfolder_out+"/"


    if os.path.isdir(Imgfolder_out) == False:
        os.makedirs(Imgfolder_out)

    for file in os.listdir(Imgfolder_in):
        if file.endswith(".png") and not file.startswith("._"):
            print(file)
            filepath = os.path.join(Imgfolder_in,file)
            img=cv2.imread(filepath,cv2.IMREAD_UNCHANGED)
            if type(img) != None:
                img_crop = FindBoundaryAndCrop(img)
                output_img_path = os.path.join(Imgfolder_out,file)
                print(output_img_path)
                cv2.imwrite(output_img_path,img_crop)
