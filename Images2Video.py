#!/usr/bin/env python3

import os
from os import listdir
from moviepy.editor import *
import numpy as np
import csv
import math
import numpy
import random
from skimage.filters import gaussian
from PIL import Image
import itertools
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout


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

a = transfx.slide_out
b = transfx.slide_in
c = transfx.crossfadein
d = transfx.crossfadeout
slide = ["bottom","top","left","right"]
effects = [a,b,c,d]

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
types=[".png","jpg",".jpeg",".wpeg"]
for images in os.listdir(folder_dir):
     for i in types:
          if images.endswith(i):        
              image.append(images)


clips=[]
#Bluring Effect Function
def blur(image):
    for list in rowsN:
        blurvalue = int(list[10]) 
        """ Returns a blurred (radius=4 pixels) version of the image """
        return gaussian(image.astype(float), sigma = blurvalue )
        
#Fetching the Images from the folder Image

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
          twidth,theight = clip.size
          if twidth > cwidth or theight > cheight or twidth < cwidth or theight < cheight:
             clip = clip.fx( vfx.resize, width = cwidth )
             
          back_clip = ImageClip("images/"+image[1])\
          .set_duration(clip_duration)
          back_clip = back_clip.fl_image( blur )
          back_clip = back_clip.fx( vfx.resize, width = cwidth )
          final = CompositeVideoClip([back_clip,clip])  
                  
          final=final.set_duration(clip_duration)
          
          value = final.start
     effect = random.choice(effects)
     pos = random.choice(slide)
     if effect == a or effect == b :
        final = final.fx(effect, duration = effectDuration, side = pos)
     else :
        final = final.fx(effect, duration = effectDuration )
        
     final = final.fx( vfx.resize, width = cwidth )      
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
          final_clip2 = final_clip2.fx( vfx.resize, newsize=(cwidth,txt_height+50) )
          
     texts.append(final_clip2)




#Putting the all clips together to make it a ready for rendering

test=[]

for (clip, text) in itertools.zip_longest(clips,texts): 
     for list in rowsN:
         clip_duration = int(list[6])
         cwidth = int(list[4]) 
         cheight = int(list[5])
         effectDuration = int(list[8])
         new_clip = CompositeVideoClip([clip,text])
         new_clip = new_clip.set_duration(clip_duration)
         finalr = new_clip.fx( vfx.resize, newsize=(cwidth,cheight) )
         
        
     test.append(finalr)




#Rendering the  video for output Review and 
#getting the data from the file name.csv
for list in rowsN:
     VideoFileName = list[0] 
     Fps = int(list[1])
     Codec = list[2]
     Audio_codec = list[3]
     
     video_clip = concatenate_videoclips(test,method="compose")
     final_clip = video_clip.fx( vfx.resize, newsize=(cwidth,cheight) )
  
     #video_clip=video_clip.resize(width = int(list),height = int(list[5]))
     final_clip.write_videofile(VideoFileName,fps = Fps,\
     remove_temp=True,codec = Codec,audio_codec = Audio_codec)
     

