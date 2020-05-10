import cv2
import pytesseract
from matplotlib import pyplot as plt

img = cv2.imread("/Users/nanzou/Documents/GitHub/walkr_collect/mission/IMG_7840.PNG",1)
plt.imshow(img)

#BGR转化为HSV
HSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#cv2.imshow("imageHSV",HSV)
plt.imshow(HSV)
#cv2.imshow('image',img)


temp_end = cv2.imread("/Users/nanzou/Documents/GitHub/walkr_collect/mission/accept_button.png", 1)
temp_hsv = cv2.cvtColor(temp_end,cv2.COLOR_BGR2HSV)
res_end = cv2.matchTemplate(img, temp_hsv, cv2.TM_CCOEFF_NORMED)
end = cv2.minMaxLoc(res_end)[1]
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_end)
cv2.rectangle(img, (0,max_loc[1]-50), (img.shape[1], max_loc[1] + 300), 0, 2)
plt.imshow(img)

mission_img = img[img.shape[1]:(max_loc[1] + 300),0:(max_loc[1]-50)]
plt.imshow(mission_img)
text = pytesseract.image_to_string(mission_img)
print(text)

'''
extract materials from text

'''


materials_planet=['Diamond','lngot']
material = materials_planet[1]

import pandas as pd
planet_list = pd.read_excel('/Users/nanzou/Documents/GitHub/walkr_collect/planet_list.xlsx',index_col=0)
planet_list[planet_list['Planet_resource']==material]