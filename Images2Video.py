#!/usr/bin/env python3

import os
from os import listdir
from moviepy.editor import *
import numpy as np
import csv
import math
import numpy
from skimage.filters import gaussian
from PIL import Image
import itertools

#Reading Data from File
textfilename = "CaptionDetails.csv"

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


outputfilename = "VideoParameters.csv"

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


def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

      
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)


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
effects=[ ]
for i in range(len(image)):
     filepath = "images/"+image[i]
     img = Image.open(filepath)
     width = img.width
     height = img.height
     for list in rowsN:
          clip_duration = int(list[6])
          cwidth = int(list[4]) 
          cheight = int(list[5])
          effectDuration = int(list[8])
          
          clip = ImageClip("images/"+image[i] )\
          .set_duration(clip_duration)
          clip = clip.set_position("center")
          clip = clip.resize(width = cwidth , height = cheight)
          if width>cwidth or height > cheight :
             clip=clip.resize(width = cwidth , height=cheight)
          back_clip = ImageClip("images/"+image[1])\
          .set_duration(clip_duration)
          back_clip = back_clip.fl_image( blur )
          back_clip = back_clip.resize(width = cwidth,height=cheight)
          final = CompositeVideoClip([back_clip,clip])
          final = final.crossfadein(effectDuration)                           
          final=final.set_duration(clip_duration)
          value = final.start
     clips.append(final)
     
texts=[]



#Fetching the Texts and its properties from the file.csv
for list  in  rows:
     CaptionText = list[1]
     TextColor =   list[3]
     FontSize = int(list[2])
     text_clip=TextClip(txt =CaptionText,color = TextColor, \
     fontsize = FontSize)
     text_clip=text_clip.set_position("center")
     for list in rowsN:
          clip_duration = int(list[6])
          cwidth = int(list[4]) 
          cheight = int(list[5])
          effectDuration = int(list[8])
          textDuration = int(list[7])
    
          txt_width,txt_height = text_clip.size
          
          color_clip = ColorClip(size = (txt_width+100,txt_height+50),
          color = (random_color))
          color_clip = color_clip.set_opacity(.3)

          final_clip = CompositeVideoClip([color_clip,text_clip]) \
          .set_position("bottom")
          final_clip1 = final_clip.set_start(value+1).\
          set_duration(textDuration).crossfadein(2.0)
          final_clip2 = final_clip1.set_duration(textDuration) \
          .crossfadeout(2.0)
          
     texts.append(final_clip2)

#Fetching the Images from the folder Image


#Putting the all clips together to make it a ready for rendering

test=[]

for (clip, text) in itertools.zip_longest(clips,texts): 
     new_clip = CompositeVideoClip([clip,text])
     new_clip = new_clip.set_duration(5)
     test.append(new_clip)

video_clip = concatenate_videoclips(test,method="compose")

#Rendering the  video for output Review and 
#getting the data from the file name.csv
for list in rowsN:
     VideoFileName = list[0] 
     Fps = int(list[1])
     Codec = list[2]
     Audio_codec = list[3]
     video_clip1=video_clip.resize(width=int(list[4]),height=int(list[5]))
     video_clip1.write_videofile(VideoFileName,fps = Fps,\
     remove_temp=True,codec = Codec,audio_codec = Audio_codec)


