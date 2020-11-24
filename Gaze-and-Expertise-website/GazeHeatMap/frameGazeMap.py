import os
from datetime import datetime, time

imageNames = os.listdir("src/images")
def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def getStartEndTime(name):
    imageInfo = [word.strip() for word in name.split("_")]
    return imageInfo[1],imageInfo[2],imageInfo[3]

def getGazePointsForScroll(coordinatesFileName):
    file = open(coordinatesFileName, "r")
    for frameName in imageNames:
        gazePoints = []
        frame_number, startTime, endTime = getStartEndTime(frameName)
        for lines in file:
            gazeInfo = [word.strip() for word in lines.split(',')]
            if is_time_between(gazeInfo[0],startTime,endTime):
                gazePoints.append(gazeInfo[1],gazeInfo[2])

        #TODO
        #Pass the gazepoints and the frameName to the heat map generator.


#Main Function to call all the other function.
#getGazePointsForScroll("report.csv")

