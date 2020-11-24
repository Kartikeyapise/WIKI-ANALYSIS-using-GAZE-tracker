"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import time
from sys import stdout
import sys
import cv2
from gaze_tracking import GazeTracking
from PyQt5 import QtGui, QtCore, QtWidgets

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Gaze Tracking'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QtWidgets.QLabel(self)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_image)
        timer.start(60)
        self.update_image()

    def update_image(self):
        pixmap = self.get_image()
        pixmap = QtGui.QImage(
            pixmap.data, pixmap.shape[1], pixmap.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QtGui.QPixmap.fromImage(pixmap))
        self.label.adjustSize()
        self.resize(pixmap.size())

    def get_image(self):
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
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

        stdout.write(f'{ls},{rs},{current_time}\n')
        return frame
        # cv2.imshow("Demo", frame)

        # if cv2.waitKey(1) == 27:
        #     break


stdout.write('Calibration ended')
app = QtWidgets.QApplication(sys.argv)
ex = App()
ex.show()
sys.exit(app.exec_())
