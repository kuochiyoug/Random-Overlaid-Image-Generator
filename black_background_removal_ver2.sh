#!/bin/bash
# Maintained by Marcus Gall marcus.gall.lw3@is.naist.jp
# Script to remove black background from object using 
# histogram bl&wh thresholds and watershed region growing


# variable definitions
#myHome=~/share/tnp_feature_matchin g/color_svm
myHome=/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/amazon_data/
imgSourceDir=$myHome/img_source

#folder structure setup
mkdir -p $myHome/auto-crop-img
mkdir -p $myHome/shapes-img
mkdir -p $myHome/bgr-img


# static cropping images to region of interest
# initial crop [crop_in_x]x[crop_in_y]+[startpoint_x]+[startpoint_y]
#for img in *.png; do convert $img \
#        -crop 2500x1900+1100+300 \
#        -resize 600 \
#crop_$img; done

cd $imgSourceDir

for dir in */ ; do
	echo "Processing $dir..."
	mkdir -p $myHome/auto-crop-img/$dir
	mkdir -p $myHome/shapes-img/$dir
	mkdir -p $myHome/bgr-img/

	echo "Auto crop objects..."
	cd $imgSourceDir/$dir
	for img in *.png; do	
		convert $img -trim  $myHome/auto-crop-img/$dir/crop_$img
	done

	echo "Calculating object's shape..."
	cd $myHome/auto-crop-img/$dir

	for img in *.png; do
		if  [[ $img == crop_* ]]; then
			base_name=${img#crop_}	
			base_name=${base_name%.png}

			convert $img \
			-blur 0x.5 \
			-normalize \
			-median 10 \
			-level 1%,6% \
			-morphology Close:2 Disk \
			-bordercolor black -border 1x1 \
		    -fill none \
			-fuzz 3% \
			-draw 'matte 0,0 floodfill' \
			-fuzz 99% -fill \#FFFFFF -opaque \#000000 \
			../../shapes-img/$dir/shape_$base_name.png; \
		fi
	done

	echo "Overlying object's with its shape..."
	cd $myHome/shapes-img/$dir

	for sh_img in *.png; do
		if  [[ $sh_img == shape_* ]]; then
			base_name=${sh_img#shape_}
			base_name=${base_name%.png}	
			convert $sh_img ../../auto-crop-img/$dir/crop_$base_name.png  $sh_img -compose multiply -composite ../../bgr-img/bgr_$base_name.png
		fi
	done
		
	echo "Applying advanced auto cut..."
	cd $myHome/bgr-img

	for img in *.png; do
		if  [[ $img == bgr_* ]]; then
			convert $img -crop \
			    `convert $img -virtual-pixel edge -blur 0x15 -fuzz 15% \
				     -trim -format '%wx%h%O' info:`   +repage   $img		
		fi
	done
		
	# cleanup, let cropped image remain for manual improvements
	#rm shape_*
done