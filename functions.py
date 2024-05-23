import cv2 
import os
import xml.etree.ElementTree as ET
# from googletrans import Translator
import time
from manga_ocr import MangaOcr
mocr = MangaOcr()
# translator = Translator()
import numpy as np
import translators as ts
import translators.server as tss
from_language, to_language = 'ja', 'zh-TW'
from PIL import Image,ImageDraw,ImageFont,ImageTk
def get_box(root):
    box=[]
    for i in root.iter('bndbox'):
        xmin=int(i.find('xmin').text)
        ymin=int(i.find('ymin').text)
        xmax=int(i.find('xmax').text)
        ymax=int(i.find('ymax').text)
        box.append([xmin,ymin,xmax,ymax])
    return box

def cv2_to_PIL(img):
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img=Image.fromarray(img)
    return img

def PIL_to_cv2(img):
    img=cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img

def crop_box(img,boxlist): #裁切圖片，給OCR辨識用 cv2 cv2
    if type(img.size)==tuple:
        img=PIL_to_cv2(img)
    x,y,w,h=boxlist
    crop_img=img[y:h,x:w]
    return crop_img

def trantext(img,language): #翻譯圖片，返回 japan和taiwan
    if type(img.size)==int:
        img1=cv2_to_PIL(img)
    japan = mocr(img1)
    to_language1=tss.papago(japan,from_language, language)
    # to_language1=translator.translate(japan,dest='zh-tw').text
    return japan,to_language1

def white_img(img,boxlist): #將img2的圖片放到img上，將文字塗白底 cv2 cv2
    if type(img.size)==tuple:
        img=PIL_to_cv2(img)
    x,y,w,h=boxlist[:4]
    img[y:h,x:w]=(255,255,255)
    return img

def aware_content_fill_single(img,mask,range=3):
    if type(img.size)==tuple:
        img=PIL_to_cv2(img)
    black_img=img.copy()
    black_img[:]=(0,0,0)
    x,y,w,h=mask
    black_img[y:h,x:w]=(255,255,255)
    black_img=cv2.cvtColor(black_img, cv2.COLOR_BGR2GRAY)
    dst=cv2.inpaint(img,black_img,range,cv2.INPAINT_TELEA)
    return dst

def text_on(img,text,x,y,fontsize,fontpath,fontrgb=(0,0,0)): #放入字體，給予單個文字
    if type(img.size)==int:
        img=cv2_to_PIL(img)
    font=ImageFont.truetype(fontpath,fontsize)
    draw=ImageDraw.Draw(img)
    draw.text((x,y),text,fill=fontrgb,font=font)
    img=draw._image
    img=PIL_to_cv2(img)
    return img

def auto_loc_put_text2(editedimg,all_info,fontpath,k=0): #給予單格對話框文字List放字，並自動調整文字大小
    imagelist=all_info[3:7]
    if type(editedimg.size)==int:
        editedimg=cv2_to_PIL(editedimg)
    word=all_info[2]
    x,y=imagelist[:2]
    w,h=imagelist[2]-imagelist[0],imagelist[3]-imagelist[1]
    x2,y2=x+w,y+h
    nowx2=x2
    now_y=y
    now_x=x

    editedimg=aware_content_fill_single(editedimg,imagelist[:4])
    font_size1=int(np.sqrt(((imagelist[2]-imagelist[0])*(imagelist[3]-imagelist[1]))*0.75/len(word)))
    ok=False
    while ok==False:
        font_loc_list=[]
        for o in range(len(word)):
            if now_y+font_size1<=y2:
                font_loc=(nowx2-font_size1,now_y)
                font_loc_list.append(font_loc)
                now_y+=font_size1
            else:
                nowx2-=font_size1
                now_y=y
                font_loc=(nowx2-font_size1,now_y)
                font_loc_list.append(font_loc)
                now_y+=font_size1
        ok=True

    for t in range(len(font_loc_list)):
        editedimg=text_on(editedimg,word[t],font_loc_list[t][0],font_loc_list[t][1],font_size1,fontpath)
    editedimg=PIL_to_cv2(editedimg)
    return editedimg

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            pass