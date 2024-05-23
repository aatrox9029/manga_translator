#%%
import os
import cv2
from yolo_txt2xml import run_txt2xml
from functions import *
from ultralytics import YOLO
clear_folder("./process/txt")
clear_folder("./process/xml")
#%%
model = YOLO('model/text_detect_yolo.pt')
input_files=os.listdir("./Input")
for i in range(len(input_files)):
    input_files[i]="Input/"+input_files[i]
results = model(input_files)

for result in results:
    result_name=(result.path.split('\\')[-1]).split('.')[0]
    result.save_txt("./process/txt/"+result_name+".txt")
run_txt2xml()
clear_folder("./process/txt")
#%%
with open('config.txt','r') as config:
    lines=config.readlines()
    language=((lines[0].split(":")[1]).replace(' ','')).replace('\n','')
    font=((lines[1].split(":")[1]).replace(' ','')).replace('\n','')

#%%
### all_info = index japanese chinese xmin ymin xmax ymax font_size clear_mode font_type ###
###              0      1        2      3 	 4 	  5   6     7          8         9       ###
xml_files=os.listdir("./process/xml/")
# language='zh-TW'

imgfolder='1'
folderpath="./Output/"+imgfolder
while os.path.isdir(folderpath):
    imgfolder=str(int(imgfolder)+1)
    folderpath="./Output/"+imgfolder
os.mkdir(folderpath)

for i in xml_files:
    root=ET.parse("./process/xml/"+i).getroot()
    boxes=get_box(root)
    img_name=root[1].text
    origin_img=cv2.imread("./Input/"+img_name,1)

    all_info=[]
    fontpath="./font/"+font
    
    for o in range(len(boxes)):
        all_info.append([0,0,0,0,0,0,0,0,0,0])
        all_info[o][0]=o
        all_info[o][3:7]=boxes[o]
        box_list=all_info[o][3:7]
        all_info[o][1],all_info[o][2]=trantext(crop_box(origin_img,box_list),language)
        origin_img=white_img(origin_img,box_list)
        origin_img=auto_loc_put_text2(origin_img,all_info[o],fontpath)
    cv2.imwrite(folderpath+"/"+img_name,origin_img)
clear_folder("./process/xml")
copy_if_not_detect("./Input",folderpath)