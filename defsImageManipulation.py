import os
import cv2

def ConvertToJPG(inImgPath):
    try:
        outImgType = ".jpg"
        name = os.path.basename(inImgPath).split('.')    
        outImg = os.path.join(os.path.dirname(inImgPath),name[0]+outImgType)
        img = cv2.imread(inImgPath)
        cv2.imwrite(outImg,img)
        os.remove(inImgPath)
        return outImg
    except:        
        return inImgPath
