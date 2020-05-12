import cv2 as cv
import os
import numpy as np
from shutil import copyfile
import random
positive_path = "Y://F_public//public//workspace//exchange//pedestrian//samplepics//new_shuxing//ped//shuxing-ped//"
negtive_path = "X://F_public//public//workspace//exchange//active_safety//linxunan//pic_fpfn//"
savepath = "X://F_public//public//workspace//exchange//active_safety//linxunan//mixup-pic//"
posCnt = 0
negCnt = 0
negImglist = os.listdir(negtive_path)
print(len(negImglist))
for files in os.listdir(positive_path):
    if '.jpg' in files:
        if os.path.exists(positive_path+files.split('.')[0]+'.xml') and os.path.exists(positive_path+files):
            posCnt +=1
            if posCnt% 2000 == 0:
                print('have finished:{}'.format(posCnt))
            if posCnt % 8 ==0:
                negCnt +=1
            if posCnt % 4 ==0:
                posImg = cv.imread(positive_path+files)
                negImg = cv.imread(negtive_path+negImglist[negCnt])
                pro = float(random.randint(1,4))/10
                dst = cv.addWeighted(posImg,(1-pro),negImg,pro,0)
                copyfile(positive_path+files.split('.')[0]+'.xml', savepath+files.split('.')[0]+'.xml')
                os.rename(savepath+files.split('.')[0]+'.xml', savepath+'mixup_'+str((1-pro))+'_'+str(posCnt)+'.xml')
                cv.imwrite(savepath+'mixup_'+str((1-pro))+'_'+str(posCnt)+'.jpg',dst)