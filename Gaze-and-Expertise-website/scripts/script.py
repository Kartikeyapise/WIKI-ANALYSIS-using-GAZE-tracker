from PIL import Image
import cv2  
import pandas as pd 
import datetime
from PIL import Image, ImageDraw
from sklearn.cluster import DBSCAN
import numpy as np

# df=pd.read_csv("./FilteredGaze.csv")
# df.columns = ['x','y','timestamp']
#-----------------------Loading Images----------------------
background = Image.open("Harvard Business School _3_17:34:53.png")
overlay1 = Image.open("mark1.png")

#-----------------------Changing Scales----------------------
background = background.convert("RGBA")
overlay1 = overlay1.convert("RGBA")


#-----------------------Saving Images----------------------
new_img1=Image.blend(background,overlay1,0.5)
new_img1.save("new1.png","PNG")

# X=df.iloc[:,0:2].values

# clustering = DBSCAN(eps=3, min_samples=5).fit(X)
# print(clustering.labels_)

# clustering

# image = cv2.imread('Harvard Business School _3_17:34:53.png')
# radius=5
# color=(0, 0, 0,0.1) 
# thickness=4
# cv2.circle(image, (505,505), radius, color, thickness) 
# # cv2.circle(image, (600,505), radius, color, thickness) 
# # cv2.circle(image, (700,505), radius, color, thickness) 
# cv2.circle(image, (505,605), radius, color, thickness) 
# cv2.circle(image, (505,705), radius, color, thickness) 



# #cv2.imshow('Test image',image)
# cv2.imwrite('testplot1.png', image)