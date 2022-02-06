#!/usr/bin/env python3

import os
from os import listdir
from moviepy.editor import *
import numpy as np
import csv

#Reading Data from File
filename = "file.csv"

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)


#generating random color
random_color=list(np.random.choice(range(255),size=3))


image = [ ]
# get the path or directory
folder_dir = "/home/pawandeep/videoclip/images"
for images in os.listdir(folder_dir):

 # check if the image end swith png or jpg or jpeg
 if (images.endswith(".png") or images.endswith(".jpg")\
        or images.endswith(".jpeg")):
        image.append(images)


clips=[]


for list  in  rows:
     text_clip=TextClip(txt ="\'"+list[1]+"\'",color= list[3],fontsize = int(list[2])  )
     text_clip=text_clip.set_position("center")
     tc_width,tc_height=text_clip.size
     color_clip=ColorClip(size=(tc_width+1000,tc_height+900),color=(random_color))
     color_clip=color_clip.set_opacity(.5)
     final_clip=CompositeVideoClip([color_clip,text_clip])
     final_clip=final_clip.set_duration(2).crossfadeout(2.0)	
     clips.append(final_clip)

for i in range(len(image)):
     clip =ImageClip("images/"+image[i] ).set_duration(2)
     clip = clip.crossfadein(2.0) 
     clips.insert(2*i+1, clip)

video_clip = concatenate_videoclips(clips,method="compose")
video_clip=video_clip.resize(width=1600,height=900)
video_clip.write_videofile("video-loop1.mp4", fps=24, remove_temp=True, codec="libx264", audio_codec="aac")


