def run_txt2xml():
    from PIL import Image
    import numpy as np
    import os
    def txt_to_xml(txt,folder,filename,path,width,height,depth):
        with open(txt,'a+')as file:
            file.write(f"<annotation>\n\t<folder>{folder}</folder>\n\t<filename>{filename}</filename>\n\t<path>{path}</path>\n\t<source>\n\t\t<database>Unknown</database>\n\t</source>\n\t<size>\n\t\t<width>{width}</width>\n\t\t<height>{height}</height>\n\t\t<depth>{depth}</depth>\n\t</size>\n\t<segmented>0</segmented>")

    def bndbox(txt,label_name,xmin, ymin, xmax, ymax):
        with open(txt,'a+')as file:
            file.write(f"\n\t<object>\n\t\t<name>{label_name}</name>\n\t\t<pose>Unspecified</pose>\n\t\t<truncated>0</truncated>\n\t\t<difficult>0</difficult>\n\t\t<bndbox>\n\t\t\t<xmin>{xmin}</xmin>\n\t\t\t<ymin>{ymin}</ymin>\n\t\t\t<xmax>{xmax}</xmax>\n\t\t\t<ymax>{ymax}</ymax>\n\t\t</bndbox>\n\t</object>")

    def end_text(txt):
        with open(txt,'a+')as file:
            file.write(f"\n</annotation>")

    def calculate_min_max(list,w,h):
        xmin_max=float(list[1])*w*2
        xmin_max_1=float(list[3])*w
        xmin=(xmin_max+xmin_max_1)/2
        xmax=xmin_max-xmin
        x_min=int(min(xmin,xmax))
        x_max=int(max(xmin,xmax))

        ymin_max=float(list[2])*h*2
        ymin_max_1=float(list[4])*h
        ymin=(ymin_max+ymin_max_1)/2
        ymax=ymin_max-ymin
        y_min=int(min(ymin,ymax))
        y_max=int(max(ymin,ymax))
        return x_min,y_min,x_max,y_max

    ### type by yourself ###
    image_path="./Input/"
    txt_path="./process/txt"

    #The labelimg classes.txt file path
    classes_txt="classes.txt"

    #labelimg_voc_output xml file will be created in this folder
    xml_path="./process/xml"
    #########################

    with open(classes_txt,'r')as file:
        label_list=[]
        for line in file.readlines():
            label_list.append(line.replace("\n",""))

    dirlist_txt=os.listdir(txt_path)
    try:
        del dirlist_txt[dirlist_txt.index('classes.txt')]
    except:
        pass

    dirlist_image=os.listdir(image_path)
    for i in dirlist_txt:
        for m in dirlist_image:
            if os.path.splitext(i)[0]==os.path.splitext(m)[0]:
                txt_file=txt_path+"/"+i
                image_file=image_path+m
                image_name=os.path.basename(image_file)
                xml_file=xml_path+"/"+os.path.splitext(image_name)[0]+".xml"

                with Image.open(image_file)as file:
                    depth=1
                    w,h=file.size[:2]
                    if len(np.array(file).shape)==3:
                        depth=(np.array(file).shape)[2]

                with open(txt_file,'r')as file:
                    txt_to_xml(xml_file,image_path,image_name,image_file,w,h,depth)
                    for line in file.readlines():
                        a=line.replace("\n","").split(" ")
                        label_name=label_list[int(a[0])]
                        xmin,ymin,xmax,ymax=calculate_min_max(a,w,h)
                        bndbox(xml_file,label_name,xmin, ymin, xmax, ymax)
                    end_text(xml_file) 