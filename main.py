#Script to loop through a given folder and all subfolders
#Intention is to save space from large image files. Most of the time I don't care about giant images.
#Downsize by saving from .bmp to jpg, or saving with a smaller resolution
#Sometimes the new file is actually larger. Don't understand why, I just included a check to see if we actually save space
#Modify starting parameters, and make sure the temp folder exists.

#Could do with some additional error handling, or check if input file is actually an image. Gives errors now when loading videos.

import cv2
import os
import shutil
import defsImageManipulation as dim #early attempt to have a library of image manipulations
import time

maxWidth = 1600
maxHeight = 1600
maxMargin = 20 #incase maxWidth or Height is 1608 or something, some margin applied to prevent unnecessary adjustments 
path = r"C:\myfolderwithimages"
tmpFolder = r"C:\tmp\resize"

tic = time.perf_counter()
for root, dirs, files in os.walk(path):    
    for file in files: 
        try:
            filePath = os.path.join(root, file)
        except:
            print('The path is invalid: ' + path)
            continue
              
        bChange = False        

        #get current extension and name
        split = file.split('.')
        name = split[0]
        ext = split[1].lower()

        #convert to jpg if bmp
        if ext == 'bmp':
            filePath = dim.ConvertToJPG(filePath)
            ext = 'jpg'

        #load image and get parameters
        try:
            img = cv2.imread(filePath)            
            width = int(img.shape[1])
            height = int(img.shape[0])
        except:
            print('The file is not a valid image: ' + filePath)
            continue

        #check if img is landscape or portrait, and limit height and width
        #apply some margin to avoid resizing only slighty and in some cases increase filesize
        if width > height:
            if width > (maxWidth + maxMargin):
                factor = width/maxWidth
                newWidth=maxWidth
                newHeight = int(height / factor)
                bChange = True
        else:
            if height > (maxHeight + maxMargin):
                factor =  height/maxHeight
                newHeight=maxHeight
                newWidth = int(width / factor)
                bChange = True

        #if image exceeded max bounds, rescale it and save in temp directly. 
        #if resized image is smaller than the original file, copy it over
        if bChange:
            curSize = os.path.getsize(filePath)

            tmpPath = os.path.join(tmpFolder, name + '.' + ext)
            scaledImg = cv2.resize(img, (newWidth, newHeight), interpolation=cv2.INTER_AREA)
            
            try:
                cv2.imwrite(tmpPath, scaledImg)
            except:
                print("Error saving image file: " + tmpPath)
                continue
                
            if os.path.getsize(tmpPath) < curSize:
                cv2.imwrite(filePath, scaledImg)
            
            try:
                os.remove(tmpPath)
            except:
                print("Error removing file: " + tmpPath)
                continue

toc = time.perf_counter()

print(f"Finished {toc - tic:0.4f} seconds")
