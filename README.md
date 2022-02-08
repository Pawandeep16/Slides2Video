# Slides2Video

# Steps to Follow

PYHTON must be installed
 
install the package installer pip for python
 
sudo apt-get -y install python3-pip

moviepy liberary must be installed to install moviepy run command

pip install moviepy
install imagemagick run the following command
sudo apt install imagemagick

goto ---- /etc/ImageMagick-6/policy.xml file  
In the file comment out the line
<policy domain="path" rights="none" pattern="@*"/>

Install scikit-image

pip install -U scikit-image

1. Put the Images in the images folder
2. Update the CSv file for text in the video.
3. Run the command --> chmod +x filename.py
4. This will make it executable
5. Run command python3 filename.py
6. play the video from folder
