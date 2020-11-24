# Need to run the file as root for Keyboard Listener on Mac OSX
import time
from datetime import datetime, timedelta
import datetime
import sys
import mss
import pytesseract
# from pynput.mouse import Listener
from pynput.keyboard import Listener, Key
import numpy
import re
import hashlib
import cv2
from PIL import Image
from reorderf import reorderFlow
import window_dimensions
import settings


class Screen(object):
    frames = {}
    scroll_value = False
    new_frame = True
    portions = []
    summary = []
    dimensions = []
    start_time = 0
    # print('Window Dimensions', dimensions)
    # browser_width = 768*2
    mw_panel = 0
    monitor = {}
    pixel_info = 0
    factor = 40
    n = 0
    data = {}  # text: coordinates, scroll
    dynamic_check = False
    articleName = ""

    def __init__(self):
        self.get_Pixels_Moved_For_Each_Keystroke()

    def get_Pixels_Moved_For_Each_Keystroke(self):
        self.factor = 40
        return

    def get_Specific_Window(self):
        img = sct.grab(self.monitor)
        # print(self.monitor)
        return img

    def capture_Frames(self):
        threshold_start = time.time()
        while not self.scroll_value:
            last_time = time.time()
            threshold = int(last_time - threshold_start)
            if not settings.keepRecording:
                break
            if threshold > 5 and self.new_frame:
                # print("threshold: ", threshold)
                self.n += 1
                window = self.get_Specific_Window()
                frame_name = str(self.articleName) + "_" + str(self.n)
                img = Image.frombytes("RGB", window.size, window.bgra, "raw", "BGRX")
                # path = "../text_extraction/Frames/"
                path = "Image_out/Frames/"
                d = datetime.datetime.now() - timedelta(seconds=5)
                output = path + str(frame_name) + "_" + d.strftime("%H:%M:%S") + ".png"
                img.save(output)
                self.new_frame = False
                break
        return

    def on_scroll(self, x, y, dx, dy):
        self.scroll_value = True
        self.new_frame = True

    def on_press(self, key):
        # print('{0} press'.format(key))
        if key == Key.down or key == Key.up:
            self.scroll_value = True
            self.new_frame = False
            # print('self.new_frame', self.new_frame)
        if key == Key.down:
            self.pixel_info += self.factor
        elif key == Key.up and self.pixel_info - self.factor > 0:
            self.pixel_info -= self.factor

    def on_release(self, key):
        # print('{0} release'.format(key))
        if key == Key.down or key == Key.up:
            self.new_frame = True
            self.scroll_value = False
            # print('self.new_frame', self.new_frame)
        if key == Key.esc:
            # Stop listener
            return False

    def on_stop_recording(self):
        print("Inside stop recording.......................................................")
        self.n += 1
        window = self.get_Specific_Window()
        frame_name = str(self.articleName)+ "_" + str(self.n)
        img = Image.frombytes("RGB", window.size, window.bgra, "raw", "BGRX")
        path = "Image_out/Frames/"
        d = datetime.datetime.now() - timedelta(seconds=5)
        output = path + str(frame_name) + "_" + d.strftime("%H:%M:%S") + "_dummy.png"
        img.save(output)

        dim_path = "File_out/Window_dim.txt"
        dimFile = open(dim_path, "w")
        dimFile.write(str(self.articleName) + " " + str(self.dimensions[2]) + " " + str(self.dimensions[3]))
        dimFile.close()

    def start_recording(self):
        listener = Listener(on_press=self.on_press, on_release=self.on_release)

        self.start_time = time.time()
        listener.start()

        self.articleName, self.dimensions = window_dimensions.get_active_window_dimensions()
        self.monitor = {"top": self.dimensions[1], "left": self.dimensions[0] + self.mw_panel,
                        "width": self.dimensions[2], "height": self.dimensions[3]}
        while True:
            with open("main_config", "r") as f:
                buffer = f.read().split()
            try:
                if buffer[1] == "no":
                    self.on_stop_recording()
                    break

            except:
                self.on_stop_recording()
                break

            else:
                if not settings.keepRecording:
                    print("keepRecording: ", settings.keepRecording)
                    break
                if self.new_frame:
                    print('Recording!')
                    self.capture_Frames()
                    # time.sleep(0.1)


if __name__ == "__main__":
    # Empty the Frames folder
    import glob
    import os

    # path = "../Integration/Image_out/Frames/"
    path = "Image_out/Frames/"
    files = glob.glob(path + '*.png')
    for f in files:
        os.remove(f)

    sc = Screen()
    with mss.mss() as sct:
        try:
            sc.start_recording()
        except KeyboardInterrupt:
            sc.on_stop_recording()
else:
    sct = mss.mss()
