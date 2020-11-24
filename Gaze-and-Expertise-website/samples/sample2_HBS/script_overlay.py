from PIL import Image
import pandas as pd 
import datetime
import cv2  
import os
from sklearn.cluster import DBSCAN
from scipy.spatial import distance
import matplotlib.pyplot as plt
import numpy as np
import csv

# p1 = (1, 2, 3)
# p2 = (4, 5, 6)
# d = distance.euclidean(p1, p2)
# print("Euclidean distance: ",d)



path=os.path.abspath(__file__)
print(path)
def get_output_img_size():
    dimensions = window_dimensions.get_active_window_dimensions()
    return dimensions

  
df=pd.read_csv("./FilteredGaze.csv")
df.columns = ['x','y','timestamp']

# bg=path+"/Image_out/Frames/_2_13:37:20.png"
background = Image.open("Harvard Business School _3_17:34:53.png")
overlay = Image.open("Harvard Business School _3_17:34:53.pngbox.png")
image = cv2.imread('Harvard Business School _3_17:34:53.png')
background = background.convert("RGBA")
overlay = overlay.convert("RGBA")


timefmt = "%H:%M:%S" 
df['timestamp'] = pd.to_datetime(df['timestamp'], format = timefmt, errors='coerce')
print(df.head())
i=0

end_time = datetime.datetime(1900, 1, 1,17, 35, 42 )
start_time = datetime.datetime(1900, 1, 1, 17, 34, 53)

#Plotting fixations based on distance
newdf=pd.DataFrame()
xnew=[]
ynew=[]
velocity=[]
j=1

while i<df.shape[0]-1 :
	#print("hello")
	if df.iloc[i,2].time() > start_time.time() and df.iloc[i,2].time() < end_time.time()  :
		# print(i,end=",")
		#Discarding the top 100 pixels due to the address bar
		if df.iloc[i,1]<=100:
			# print("Hello")
			i=i+1
			continue
		else:
			#Creating new dataframes forc lustering
			xnew.append(df.iloc[i,0])
			ynew.append(df.iloc[i,1])

			#Calculating pairwise euclidean distance
			p1=(df.iloc[i,0], df.iloc[i,1])
			p2=(df.iloc[i+1,0], df.iloc[i+1,1])
			d = distance.euclidean(p1, p2)

			#Calculating velocity
			t=1.0/30
			velocity.append(d/t)

			#Plotting fixations based on distance metric
			if(d<=10):
				if(j==1):
					time_to_first_fixation= df.iloc[i,2]-start_time
					print("Time to first fixation in seconds: "+(str)(time_to_first_fixation.total_seconds()))
				#print("Euclidean distance: ",d)
				center_coordinates = (df.iloc[i,0], df.iloc[i,1]) 
				radius=6
				color=(175, 22, 86) 
				thickness=2
				cv2.circle(image, center_coordinates, radius, color, thickness)
				j=j+1 
	i=i+1

#----------------------CLUSTERING SECTION FOR FIXATIONS----------------
#performing scale inversion to plot correctly
ymod = []
t = max(ynew)
minval = min(ynew)
for i in ynew:
    temp = i
    i = i-t
    i = (-1)*i
    # print(str(temp)+": "+str(i))
    ymod.append(i+minval)
# print(ymod)

newdf['x']=xnew
newdf['y']=ymod
print(newdf.head())
#DBSCAN Clustering to reveal fixation points
db = DBSCAN(eps=3, min_samples=2).fit(newdf)
print(db.labels_)

#---------------------Plotting clusters-----------------
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)
new_np = newdf.to_numpy()



plt.figure(figsize=(13.11,7.41),dpi=100)
# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 0]

    class_member_mask = (labels == k)

    xy = new_np[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

#     xy = new_np[class_member_mask & ~core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
#              markeredgecolor='k', markersize=6)

#plt.title('Estimated number of clusters: %d' % n_clusters_)

plt.savefig('mark1.png')
# plt.show()






#---------------Saving Files and Image ---------------

#Saving Velocity File
with open('velocity.txt', 'w') as filehandle:
    for listitem in velocity:
        filehandle.write('%s\n' % listitem)

cv2.imwrite('testplot.png', image)
#Overlaying the heatmap
new_img = Image.blend(background, overlay, 0.5)
new_img.save("new.png","PNG")


