import cv2 as cv
import os
import numpy as np
from shutil import copyfile
import random
import xml.etree.ElementTree as ET
positive_path = "Y://F_public//public//workspace//exchange//pedestrian//samplepics//new_shuxing//ped//shuxing-ped//"
negtive_path = "X://F_public//public//workspace//exchange//active_safety//linxunan//pic_fpfn//"
savepath = "X://F_public//public//workspace//exchange//active_safety//linxunan//mixup-pic//"

def simulation():
    path ="X://F_public//public//workspace//exchange//active_safety//linxunan//mixup-pic//"
    for info in os.listdir(path):
        if '.jpg' in info:
            img = cv.imread(path+info)
            tree = ET.parse(path+info.split('.jpg')[0]+'.xml')
            root = tree.getroot()
            for ob in root.findall('object'):
                for bndbox in ob.iter('bndbox'):
                    for xmin in bndbox.iter('xmin'):
                        xmin = int(xmin.text)
                    for ymin in bndbox.iter('ymin'):
                        ymin = int(ymin.text)
                    for xmax in bndbox.iter('xmax'):
                        xmax = int(xmax.text)
                    for ymax in bndbox.iter('ymax'):
                        ymax = int(ymax.text)
                    cv.rectangle(img, (xmin,ymin), (xmax,ymax), (0,255,255), 2, 1)
            cv.imshow("image",img)
        cv.waitKey(0)

def main():
    posCnt = 0
    negCnt = 0
    negImglist = os.listdir(negtive_path)
    for files in os.listdir(positive_path):
        if '.jpg' in files:
            if os.path.exists(positive_path+files.split('.')[0]+'.xml') and os.path.exists(positive_path+files):
                posCnt +=1
                if posCnt% 2000 == 0:
                    print('have finished:{}'.format(posCnt))
                if posCnt % 8 ==0:
                    negCnt +=1
                if posCnt % 4 ==0:
                    # print("posiImg:",files)
                    # print("negImglist:", negImglist[negCnt])
                    posImg = cv.imread(positive_path+files)
                    negImg = cv.imread(negtive_path+negImglist[negCnt])
                    if not np.shape(posImg) == np.shape(negImg):
                        negImg = cv.resize(negImg,(np.shape(posImg)[1],np.shape(posImg)[0]))
                    pro = float(random.randint(2,6))/10
                    dst = cv.addWeighted(posImg,(1-pro),negImg,pro,0)
                    copyfile(positive_path+files.split('.')[0]+'.xml', savepath+files.split('.')[0]+'.xml')
                    os.rename(savepath+files.split('.')[0]+'.xml', savepath+'mixup_'+str((1-pro))+'_'+str(posCnt)+'.xml')
                    cv.imwrite(savepath+'mixup_'+str((1-pro))+'_'+str(posCnt)+'.jpg',dst)
main()