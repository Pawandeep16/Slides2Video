#!/usr/bin/env python3

import os
from os import listdir
from moviepy.editor import *
import numpy as np
import csv
from skimage.filters import gaussian
from PIL import Image


#Reading Data from File
textfilename = "file.csv"

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
with open(textfilename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)


outputfilename = "name.csv"

# initializing the titles and rows list
fieldsN = []
rowsN = []

# reading csv file
with open(outputfilename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    # extracting field names through first row
    fieldsN = next(csvreader)
    # extracting each data row one by one
    for row in csvreader:
        rowsN.append(row)



#generating random color
random_color=list(np.random.choice(range(255),size=3))


image = [ ]
# get the path or directory
folder_dir = os.getcwd()+"/images"

for images in os.listdir(folder_dir):

 # check if the image end swith png or jpg or jpeg
 if (images.endswith(".png") or images.endswith(".jpg")\
        or images.endswith(".jpeg")):
        image.append(images)


clips=[]
#Bluring Effect Function
def blur(image):
    """ Returns a blurred (radius=4 pixels) version of the image """    
    return gaussian(image.astype(float), sigma=4)


#Fetching the Texts and its properties from the file.csv
for list  in  rows:
     text_clip=TextClip(txt ="\'"+list[1]+"\'",color= list[3],fontsize = int(list[2]) )
     text_clip=text_clip.set_position("center")
     for list in rowsN:
          text_clip = text_clip.resize(width=int(list[4])-50 )
          color_clip=ColorClip(size=(int(list[4]),int(list[5]) ),color=(random_color))
          color_clip=color_clip.set_opacity(.5)

     final_clip=CompositeVideoClip([color_clip,text_clip])
     final_clip=final_clip.set_duration(2).crossfadeout(2.0)
     clips.append(final_clip)

#Fetching the Images from the folder Image    
for i in range(len(image)):
     filepath = "images/"+image[i]
     img = Image.open(filepath)
     width = img.width
     height = img.height
     clip =ImageClip("images/"+image[i] ).set_duration(2)
     clip=clip.set_position("center")
     for list in rowsN:
          clip=clip.resize(width =int(list[4]),height=int(list[5]))
          back_clip =ImageClip("images/"+image[1]).set_duration(2)
          back_clip = back_clip.fl_image( blur )
          back_clip=back_clip.resize(width=int(list[4]),height=int(list[5]))

     final=CompositeVideoClip([back_clip,clip])
     final=final.set_duration(2).crossfadein(2.0)
     clips.insert(2*i+1,final) 

#Putting the all clips together to make it a ready for rendering 
video_clip = concatenate_videoclips(clips,method="compose")

#Rendering the  video for output Review and getting the data from the file name.csv 
for list in rowsN:
    video_clip1=video_clip.resize(width=int(list[4]),height=int(list[5]))
    video_clip1.write_videofile( list[0] , fps= int(list[1]), remove_temp=True, codec=list[2], audio_codec=list[3])


