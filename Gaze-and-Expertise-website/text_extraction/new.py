import time
import cv2
import mss
import numpy as np
from PIL import Image

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {'top': 27, 'left': 67, 'width': 1853, 'height': 1173}

    last_time = time.time()

    # Get raw pixels from the screen, save it to a Numpy array
    sct_img = sct.grab(monitor)
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    output = "monitor-{}.png"
    img.save(output)



# import mss
# from PIL import Image
#
#
# with mss.mss() as sct:
#     # Get rid of the first, as it represents the "All in One" monitor:
#     for num, monitor in enumerate(sct.monitors[1:], 1):
#         # Get raw pixels from the screen
#         sct_img = sct.grab(monitor)
#
#         # Create the Image
#         img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
#         # The same, but less efficient:
#         # img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
#
#         # And save it!
#         output = "monitor-{}.png".format(num)
#         img.save(output)
#         print(output)