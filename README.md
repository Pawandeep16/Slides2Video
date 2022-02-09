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

"policy domain="path" rights="none" pattern="@*" 
  you can found this at the bottom part of the file

Install scikit-image

pip install -U scikit-image

install pillow using command as follow

python3 -m pip install --upgrade Pillow

1. Put the Images in the images folder
2. Update the CSv file for text in the video.
3. Run the command --> chmod +x filename.py
4. This will make it executable
5. Run command python3 filename.py
6. play the video from folder

#For Windows OS
- You any editor or compiler like Visual Studio Code or pycharm  
- Pyhton must be installed 
- then pip must be installed
- follow this to install pip https://www.geeksforgeeks.org/how-to-install-pip-on-windows/
- install moviepy using command in the command prompt    pip install moviepy
- ImageMagick must be installed download the imagemagick and install manually from this site https://imagemagick.org/script/download.php#windows
- Now update the directory  C:\Python39\Lib\site-packages\moviepy  open file name config_defaults.py
- paste this    IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\magick.exe"
- install skit  using command  pip install -U scikit-image
- Clone the project  
- open the even.py file 
- Remove the very first Line 
- run the script 
- Enjoy the Video
