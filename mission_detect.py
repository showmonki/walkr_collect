import cv2
import pytesseract
from matplotlib import pyplot as plt
import re
import pandas as pd

img = cv2.imread("/Users/nanzou/Documents/GitHub/walkr_collect/mission/IMG_7840.PNG",1)
plt.imshow(img)

#BGR changed to HSV
HSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#cv2.imshow("imageHSV",HSV)
plt.imshow(HSV)
#cv2.imshow('image',img)

## match pattern for accept button
temp_end = cv2.imread("/Users/nanzou/Documents/GitHub/walkr_collect/mission/accept_button.png", 1)
temp_hsv = cv2.cvtColor(temp_end,cv2.COLOR_BGR2HSV)
res_end = cv2.matchTemplate(img, temp_hsv, cv2.TM_CCOEFF_NORMED)
end = cv2.minMaxLoc(res_end)[1]
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_end)

'''
## rectangle to test range
cv2.rectangle(img, (0,max_loc[1]-50), (img.shape[1], max_loc[1] + 300), 0, 2)
plt.imshow(img)
'''

mission_img = img[img.shape[1]:(max_loc[1] + 300),0:(max_loc[1]-50)]
plt.imshow(mission_img)
mission_hsv = cv2.cvtColor(mission_img,cv2.COLOR_BGR2HSV)

'''
## extract materials from text
with structure
lower = [26]
upper = [32]
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
im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(mask.shape)
#print(mask[0])
print(len(contours))
cv2.drawContours(mission_hsv, contours, -1, (0, 0, 255), 1)
for i in contours:
    print(cv2.contourArea(i))  # 计算缺陷区域面积
    x, y, w, h = cv2.boundingRect(i)  # 画矩形框
    cv2.rectangle(mission_hsv, (x, y), (x + w, y + h), (0, 255, 0), 1)
#cv.imwrite(show_result_path, match_img_color)
plt.imshow(mission_hsv)




thre = mission_img.mean()
 
# -100 - 100
contrast = -155.0
 
img_out = mission_img * 1.0
 
if contrast <= -255.0:
    img_out = (img_out >= 0) + thre -1
elif contrast > -255.0 and contrast < 0:
    img_out = mission_img + (mission_img - thre) * contrast / 255.0   
elif contrast < 255.0 and contrast > 0:    
    new_con = 255.0 *255.0 / (256.0-contrast) - 255.0
    img_out = mission_img + (mission_img - thre) * new_con / 255.0   
else:
    mask_1 = mission_img > thre 
    img_out = mask_1 * 255.0
 
img_out = img_out / 255.0 
 
# 饱和处理
mask_1 = img_out  < 0 
mask_2 = img_out  > 1
 
img_out = img_out * (1-mask_1)
img_out = img_out * (1-mask_2) + mask_2
 
plt.figure()
plt.imshow(mission_img/255.0)
plt.axis('off')
 
plt.figure(2)
plt.imshow(img_out)
plt.axis('off')


text = pytesseract.image_to_string(mission_img_structure)
print(text)
'''


materials_planet=['Diamond','lngot']
material = materials_planet[1]

## lngot should be Ingot. Need compare text similarity


planet_list = pd.read_excel('/Users/nanzou/Documents/GitHub/walkr_collect/planet_list.xlsx',index_col=0)
planet_list[planet_list['Planet_resource']==material]