import os
import glob
from PIL import Image, ImageOps
import pandas as pd 
import datetime
import cv2  
from scipy.spatial import distance
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import numpy as np
import csv

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def convert_date_time(startTime,endTime):
    startInfo=[word.strip() for word in startTime.split(":")]
    endInfo=[word.strip() for word in endTime.split(":")]
    
    #converting time to date_time format
    start_time = datetime.datetime(1900, 1, 1,int(startInfo[0]),int(startInfo[1]), int(startInfo[2]) )
    end_time = datetime.datetime(1900, 1, 1, int(endInfo[0]),int(endInfo[1]),int(endInfo[2]))
    return start_time, end_time


def getStartTime(name):
    imageInfo = [word.strip() for word in name.split("_")]
    startTime = [word.strip() for word in imageInfo[2].split(".")]
    return imageInfo[1], startTime[0]

def plot_overlay(frame_number,frameName,start_time,end_time):

    #opening background image
    path1=os.getcwd()
    path1=path1+"/Image_out/Frames/"+frameName
    background = Image.open(path1)
    
    #opening overlay image
    path1=os.getcwd()
    path1=path1+"/Image_out/"+frameName+"box.png"
    overlay = Image.open(path1)
    # print("Overlay opened successfully")
    
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    #blending the heat maps
    background = ImageOps.fit(background, overlay.size, Image.ANTIALIAS)

    new_img = Image.blend(background, overlay, 0.5)
    path1=os.getcwd()
    path1=path1+"/Image_out/Overlays/"+frameName
    new_img.save(path1,"PNG")
    
    # ================================================



    # image = cv2.imread('_2_13:37:20.png')

def plot_fixation(frame_number,frameName,start_time,end_time,csv_file):
    #Reading gaze file
    df=pd.read_csv("./File_out/FilteredGaze.csv")
    df.columns = ['x','y','timestamp']
    #opening background image
    path1=os.getcwd()
    path1=path1+"/Image_out/Frames/"+frameName
    image = cv2.imread(path1)
    image1=cv2.imread(path1)
    #Modifications to datafram
    timefmt = "%H:%M:%S" 
    df['timestamp'] = pd.to_datetime(df['timestamp'], format = timefmt, errors='coerce')
    i=0
    #Plotting fixations based on distance
    newdf=pd.DataFrame()
    xnew=[]
    ynew=[]
    j=1
    count=0
    time_to_first_fixation=df.iloc[i,2]
    #Path for fixations folder
    path=os.getcwd()
    path=path+"/Image_out/Fixations/"+frame_number+".txt"

    while i<df.shape[0]-1 :
        if df.iloc[i,2].time() > start_time.time() and df.iloc[i,2].time() < end_time.time()  :
            #Discarding the top 100 pixels due to the address bar
            center_coordinates = (df.iloc[i,0], df.iloc[i,1]) 
            radius=6
            color=(0, 0, 255) 
            thickness=2
            

            count=count+1
            if df.iloc[i,1]<=100:
                i=i+1
                continue
            else:
                cv2.circle(image1, center_coordinates, radius, color, thickness)
                #Creating new dataframes forc lustering
                xnew.append(df.iloc[i,0])
                ynew.append(df.iloc[i,1])
                #Calculating pairwise euclidean distance
                p1=(df.iloc[i,0], df.iloc[i,1])
                p2=(df.iloc[i+1,0], df.iloc[i+1,1])
                d = distance.euclidean(p1, p2)
                #Plotting fixations based on distance metric
                
                if(d<=10):
                    if(j==1):
                        time_to_first_fixation= df.iloc[i,2]-start_time
                        with open(path, 'w') as filehandle:
                            filehandle.write("Time to first fixation in seconds:"+str(time_to_first_fixation.total_seconds())+"\n")
                    cv2.circle(image, center_coordinates, radius, color, thickness)
                    j=j+1 

                
        i=i+1

    with open(path, 'a+') as filehandle:
        filehandle.write("Gaze points found:"+str(count)+"\n")
        filehandle.write("Euclidean fixations found:"+str(j)+"\n")
    csv_file.write(str(count)+ "," +str(time_to_first_fixation.total_seconds())+ "," +str(j)+",")   
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
    newdf['y']=ynew
    # print(newdf.head())
    #DBSCAN Clustering to reveal fixation points
    db = DBSCAN(eps=3, min_samples=2).fit(newdf)
    

    # print(db.labels_)

    #---------------------Plotting clusters-----------------
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    with open(path, 'a+') as filehandle:
        filehandle.write("\nNumber of DBSCAN Clusters: "+str(len(set(labels)))+"\n")
    csv_file.write(str(len(set(labels)))+ "," ) 
    with open(path, 'a+') as filehandle:
        filehandle.write(str(db.labels_))
    
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
        plt.ylim((0,800))
        plt.xlim((0,1000))
        # plt.xticks(rotation=180)
        # plt.yticks(rotation=180)
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

    #Storing all the plots
    path2=os.getcwd()
    path3=path2+"/Image_out/Fixations/"+frame_number+".png"
    path4=path2+"/Image_out/Fixations/"+frame_number+"_dbscan.png"
    path5=path2+"/Image_out/Fixations/"+frame_number+"_original.png"
    path6=path2+"/Image_out/Fixations/"+frame_number+"_dbscan_flip.png"
    plt.savefig(path4)
    cv2.imwrite(path3, image)
    cv2.imwrite(path5, image1)

    im_plot= cv2.imread(path4)
    img_rotate= cv2.flip(im_plot, 0)
    cv2.imwrite(path6,img_rotate)
    

    path1=os.getcwd()
    path1=path1+"/Image_out/Fixations/"+frame_number+"_original.png"
    background = Image.open(path1)
    path1=os.getcwd()
    path1=path1+"/Image_out/"+frameName+"box.png"
    overlay = Image.open(path1)
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")
    background = ImageOps.fit(background, overlay.size, Image.ANTIALIAS)
    new_img = Image.blend(background, overlay, 0.5)
    path1=os.getcwd()
    path1=path1+"/Image_out/Overlays/fixations_"+frameName
    new_img.save(path1,"PNG")


def store_velocity(frame_number,frameName,start_time,end_time,csv_file):
    
    df=pd.read_csv("./File_out/FilteredGaze.csv")
    df.columns = ['x','y','timestamp']
    timefmt = "%H:%M:%S" 
    df['timestamp'] = pd.to_datetime(df['timestamp'], format = timefmt, errors='coerce')
    i=0
    velocity=[]
    while i<df.shape[0]-1 :
        if df.iloc[i,2].time() > start_time.time() and df.iloc[i,2].time() < end_time.time()  :
            #Discarding the top 100 pixels due to the address bar
            if df.iloc[i,1]<=100:
                # print("Hello")
                i=i+1
                continue
            else:
                #Calculating pairwise manhattan distance
                p1=(df.iloc[i,0], df.iloc[i,1])
                p2=(df.iloc[i+1,0], df.iloc[i+1,1])
                d = distance.euclidean(p1, p2)
                if df.iloc[i+1,0] - df.iloc[i,0] <0:
                    d=d*-1;
                #Calculating velocity
                t=1.0/30
                velocity.append(round(d/t,2))
        i=i+1

    #Storing the velocity file
    path1=os.getcwd()
    path1=path1+"/Image_out/Velocity/"+frame_number+".txt"
    csv_file.write(str(max(velocity))+","+str(min(velocity))+"\n")
    with open(path1, 'w') as filehandle:
        for listitem in velocity:
            filehandle.write('%s\n' % listitem)

def open_images(articleName_csv, count, ratio):
    frameDict = {}
    frameNum = []
    imageNames = os.listdir("./Image_out/Frames/")

    #Removing older overlays
    path="./Image_out/Overlays/"
    files=glob.glob(path+'*.png')
    for f in files:
        os.remove(f)

    #Removing older velocity files
    path="./Image_out/Velocity/"
    files=glob.glob(path+'*.txt')
    for f in files:
        os.remove(f)

    #Removing older fixation files
    path="./Image_out/Fixations/"
    files=glob.glob(path+'*.txt')
    for f in files:
        os.remove(f)
    files=glob.glob(path+'*.png')
    for f in files:
        os.remove(f)
    
    
    for frames in imageNames:
        if frames.__contains__(".png"):
            frame_number, startTime = getStartTime(frames)
            frameNum.append(int(frame_number))
            frameDict[int(frame_number)] = startTime
    
    csv_file = open("./data_collected.csv", "a+")

    frameNum.sort()
    lastFrame = frameNum[-1]
    for frameName in imageNames:
        
        if frameName.__contains__("dummy"):
            continue
        frame_number, startTime = getStartTime(frameName)
        endTime = frameDict[int(frame_number) + 1]
        print("Frame number :" + str(frame_number))
        start_time,end_time=convert_date_time(startTime,endTime)
        csv_file.write(str(articleName_csv)+"," +str(count)+"," + str(ratio)+"," + str(frame_number)+"," )
        plot_overlay(frame_number,frameName,start_time,end_time)
        plot_fixation(frame_number,frameName,start_time,end_time,csv_file)
        store_velocity(frame_number,frameName,start_time,end_time,csv_file)
    
    csv_file.close()
        

if __name__ == "__main__":
    open_images()