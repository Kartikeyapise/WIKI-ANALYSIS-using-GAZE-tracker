"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import time
from sys import stdout
import sys
import cv2
from GazeTracking.gaze_tracking import GazeTracking
from GazeTracking.summary.gazePlotMap import gPMain
from GazeTracking.summary.createSummary import crMain
import threading


class Tracker(object):
    def __init__(self):
        print('-------------------- NEW TRACKER INITIALIZED -------------------- ')
        self.gaze = GazeTracking()
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        self.running = True

        import os
        if not os.path.exists('output'):
            os.makedirs('output')

        if os.path.isfile('output/main_config'):
            with open("output/main_config", "r") as f:
                buffer = f.read().split()
        else:
            buffer = ['', '']

        with open("output/main_config", "w") as f:
            buffer[0] = "yes"
            buffer[1] = "yes"
            f.write("\n".join(buffer))

        if os.path.exists('output/FinalGaze.csv'):
            os.remove('output/FinalGaze.csv')
        with open("output/FinalGaze.csv", "w") as f:
            f.write('')
        threading.Thread(target=self.update, args=()).start()

        import subprocess
        self.fRecord = subprocess.Popen(
            ["python3", "./GazeTracking/text_extraction/Frame_recording.py"])

    def stop(self):
        self.running = False
        self.video.release()
        with open("output/main_config", "r") as f:
            buffer = f.read().split()

        with open("output/main_config", "w") as f:
            buffer[0] = "no"
            buffer[1] = "no"
            f.write("\n".join(buffer))
        gPMain()
        crMain()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while self.running:
            time.sleep(.06)
            # We get a new frame from the webcam
            (self.grabbed, frame) = self.video.read()
            # We send this frame to GazeTracking to analyze it
            self.gaze.refresh(frame)
            frame = self.gaze.annotated_frame()
            text = ""

            if self.gaze.is_blinking():
                text = "Blinking"
            elif self.gaze.is_right():
                text = "Looking right"
            elif self.gaze.is_left():
                text = "Looking left"
            elif self.gaze.is_center():
                text = "Looking center"

            cv2.putText(frame, text, (90, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

            left_pupil = self.gaze.pupil_left_coords()
            right_pupil = self.gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130),
                        cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165),
                        cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            ls = 0
            if left_pupil != None:
                ls = left_pupil[0]
            rs = 0
            if right_pupil != None:
                rs = right_pupil[0]

            now = time.localtime()
            current_time = time.strftime("%H:%M:%S", now)
            with open("output/FinalGaze.csv", "a") as f:
                f.write(f'{ls},{rs},{current_time}\n')
            self.frame = frame
