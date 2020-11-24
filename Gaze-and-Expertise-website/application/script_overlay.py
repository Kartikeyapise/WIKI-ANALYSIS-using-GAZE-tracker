from PIL import Image
import pandas as pd 
import datetime
import cv2  
import os
from scipy.spatial import distance



p1 = (1, 2, 3)
p2 = (4, 5, 6)
d = distance.euclidean(p1, p2)
print("Euclidean distance: ",d)



path=os.path.abspath(__file__)
print(path)
def get_output_img_size():
    dimensions = window_dimensions.get_active_window_dimensions()
    return dimensions

  
df=pd.read_csv("./File_out/FilteredGaze.csv")
df.columns = ['x','y','timestamp']

# bg=path+"/Image_out/Frames/_2_13:37:20.png"
background = Image.open("_2_13:37:20.png")
overlay = Image.open("_2_13:37:20_out.png")
image = cv2.imread('_2_13:37:20.png')
background = background.convert("RGBA")
overlay = overlay.convert("RGBA")


timefmt = "%H:%M:%S" 
df['timestamp'] = pd.to_datetime(df['timestamp'], format = timefmt, errors='coerce')
print(df.head())
i=0

end_time = datetime.datetime(1900, 1, 1, 13, 37, 46)
start_time = datetime.datetime(1900, 1, 1, 13, 37, 20)

while i<df.shape[0] and df.iloc[i,2].time() > start_time.time() and df.iloc[i,2].time() < end_time.time()  :
	#print("hello")
	if :
		# print(i,end=",")
		center_coordinates = (df.iloc[i,0], df.iloc[i,1]) 
		radius=5
		color=(0, 0, 0) 
		thickness=-1
		cv2.circle(image, center_coordinates, radius, color, thickness) 
	i=i+1

#cv2.imshow('Test image',image)
cv2.imwrite('testplot.png', image)

new_img = Image.blend(background, overlay, 0.5)
new_img.save("new.png","PNG")