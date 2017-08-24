#Put this path to amazons data
#-------------------------
ImageSource=/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/amazon_data/img_source
Scripts_folder=/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools
#nobackground_Images=/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/amazon_data/nobackground
Resized_Images=/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/amazon_data/img_resize
#------------------------




export PYTHONPATH="/usr/local/lib/python3.5/dist-packages:$PYTHONPATH"
item_folder=/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/items_fast/
mkdir $item_folder
cp $Resized_Images/*.png $item_folder


GeneratedData=/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/data_fast_train/
GeneratedImageData=$GeneratedData"images/"
GeneratedAnnoData=$GeneratedData"annotation/"
GeneratedData_Test=/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/data_fast_Test/
GeneratedImageData_Test=$GeneratedData_Test"images/"
GeneratedAnnoData_Test=$GeneratedData_Test"annotation/"



#image_generate_fast_training.py [item_folder] [data_out] [sets] [sample] [items_per]
python3 $Scripts_folder/image_generate_fast_training.py $item_folder $GeneratedData 5 100 15
python3 $Scripts_folder/image_generate_fast_training.py $item_folder $GeneratedData_Test 1 160 1



export PYTHONPATH="/usr/local/lib/python3.5/dist-packages:$PYTHONPATH"
rm ./net/yolo/parse-history.txt


FolderRoot="/root/share/FastTraining/"
seed=1234
name_of_net="arc2017_56classes"
AdditionalDescription="_PretrainedWeight"

ResultRoot=$FolderRoot"TrainingResult/"
mkdir $ResultRoot
ResultFolder=$ResultRoot$name_of_net"_seed"$seed$AdditionalDescription"/"
mkdir $ResultFolder

SummaryFolder=$ResultFolder"summary/"
mkdir $SummaryFolder

Ckpt=$ResultFolder"ckpt/"
mkdir $Ckpt

#cp /root/share/40classesReal_Bin_New0715/TrainingResult/arc2017_40classes_seed1234_PretrainedWeight/ckpt/* $Ckpt

Log=$ResultFolder"log.txt"


# With Pretrained Weight
python3 ../flow_ARC2017Settings --train \
                        --model "./cfg/"$name_of_net".cfg" \
                        --load "-1" \
                        --dataset $GeneratedImageData \
                        --annotation $GeneratedAnnoData \
                        --test_accuracy_dataset $GeneratedImageData_Test \
                        --test_accuracy_annotation $GeneratedAnnoData_Test \
                        --label "/root/catkin_ws/src/tnp/yolo_light/scripts/AnnoImageTools/data_fast_train/labels.txt" \
                        --log $Log \
                        --backup $Ckpt \
                        --summary $SummaryFolder \
                        --lr "0.005" \
                        --seed $seed \
                        --noiselevel "0" \
                        --blur "4" \
                        --gamma "0" \
                        --saturation "0.1" \
                        --exposure "0.2" \
                        --trainer "adam" \
                        --keep "50" \
                        --batch "50" \
                        --epoch "2000" \
                        --save "100" \
                        --gpu "0.0" \
                        --use_gpu_num "3"
