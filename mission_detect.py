import cv2
import pytesseract
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

img = cv2.imread("./walkr_collect/mission/IMG_7840.PNG",1)
plt.imshow(img)

#BGR changed to HSV
HSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#cv2.imshow("imageHSV",HSV)
plt.imshow(HSV)
#cv2.imshow('image',img)

## match pattern for accept button
temp_end = cv2.imread("./walkr_collect/mission/accept_button.png", 1)
temp_hsv = cv2.cvtColor(temp_end,cv2.COLOR_BGR2HSV)
res_end = cv2.matchTemplate(img, temp_hsv, cv2.TM_CCOEFF_NORMED)
end = cv2.minMaxLoc(res_end)[1]
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_end) #max_loc

'''
## rectangle to test range
cv2.rectangle(img, (0,max_loc[1]-50), (img.shape[1], max_loc[1] + 300), 0, 2)
plt.imshow(img)
'''

mission_img = img[(max_loc[1]-50):(max_loc[1] + 300),0:(max_loc[1])-50,].copy() # Y, X,RGB
plt.imshow(mission_img)
#mission_hsv = cv2.cvtColor(mission_img,cv2.COLOR_BGR2HSV)
missiion_img_copy = mission_img.copy()

## extract materials from text with structure
lower = [40,30,10]
upper = [48,36,17]
lower = np.array(lower, dtype="uint8")  # 颜色下限
upper = np.array(upper, dtype="uint8")  # 颜色上限
# 根据阈值找到对应颜色
mask = cv2.inRange(mission_img, lower, upper)    #查找处于范围区间的
#mask = 255-mask                          #留下铝材区域
output = cv2.bitwise_and(mission_img, mission_img, mask=mask)    #获取铝材区域
#bgroutput = cv2.cvtColor(output,cv2.COLOR_HSV2BGR)
# 展示图片
plt.imshow(np.hstack([mission_img, output]))
#plt.imshow(np.hstack([mission_img, bgroutput]))

contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #RETR_TREE,RETR_EXTERNAL
#print(mask.shape)
#print(mask[0])
#print(len(contours))
cv2.drawContours(missiion_img_copy, contours, -1, (0, 255,0), 1)
plt.imshow(missiion_img_copy)


lower = [35,30,10]
upper_2 = [50,36,17]
lower = np.array(lower, dtype="uint8")  # 颜色下限
upper_2 = np.array(upper_2, dtype="uint8")  # 颜色上限
# 根据阈值找到对应颜色
mask_2 = cv2.inRange(output, lower, upper_2)    #查找处于范围区间的
#mask_2 = 255-mask_2                          #留下铝材区域
output_2 = cv2.bitwise_and(output, output, mask=mask_2)    #获取铝材区域
#bgroutput = cv2.cvtColor(output,cv2.COLOR_HSV2BGR)
# 展示图片
plt.imshow(np.hstack([mission_img, output_2]))

edged = cv2.Canny(missiion_img_copy, 10, 5)
plt.imshow(edged)
#https://blog.csdn.net/m0_37857300/article/details/84973197?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase



text = pytesseract.image_to_string(missiion_img_copy)
print(text)



materials_planet=['Diamond','lngot']
material = materials_planet[1]

## lngot should be Ingot. Need compare text similarity


planet_list = pd.read_excel('./walkr_collect/planet_list.xlsx',index_col=0)
planet_list[planet_list['Planet_resource']==material]