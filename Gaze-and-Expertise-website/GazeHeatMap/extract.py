# import cv2

# img = cv2.imread('out_check200.png')

# fromCenter = False
# ROIs = cv2.selectROIs('Select ROIs', img, fromCenter)

# ROI_1 = img[ROIs[0][1]:ROIs[0][1]+ROIs[0][3], ROIs[0][0]:ROIs[0][0]+ROIs[0][2]]
# ROI_2 = img[ROIs[1][1]:ROIs[1][1]+ROIs[1][3], ROIs[1][0]:ROIs[1][0]+ROIs[1][2]]
# ROI_3 = img[ROIs[2][1]:ROIs[2][1]+ROIs[2][3], ROIs[2][0]:ROIs[2][0]+ROIs[2][2]]

# cv2.imshow('1', ROI_1)
# cv2.imshow('2', ROI_2)
# cv2.imshow('3', ROI_3)

# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np

# import image
image = cv2.imread('out_check200.png')

# # grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray', gray)

# # binary
# ret, thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('threshold', thresh)

# # dilation
# kernel = np.ones((10, 1), np.uint8)
# img_dilation = cv2.dilate(thresh, kernel, iterations=1)
# cv2.imshow('dilated', img_dilation)

roi_copy = image.copy()
roi_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
# filter black color
mask1 = cv2.inRange(roi_hsv, np.array([0, 0, 0]), np.array([180, 255, 125]))
mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
mask1 = cv2.Canny(mask1, 100, 300)
mask1 = cv2.GaussianBlur(mask1, (1, 1), 0)
mask1 = cv2.Canny(mask1, 100, 300)

# find contours
# cv2.findCountours() function changed from OpenCV3 to OpenCV4: now it have only two parameters instead of 3
cv2MajorVersion = cv2.__version__.split(".")[0]
# check for contours on thresh
if int(cv2MajorVersion) >= 4:
    ctrs, hier = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
else:
    im2, ctrs, hier = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# sort contours
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

for i, ctr in enumerate(sorted_ctrs):
    if cv2.contourArea(ctr) > 100:

        peri = cv2.arcLength(ctr, True)
        approx = cv2.approxPolyDP(ctr, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        print(x,y, cv2.contourArea(ctr))
        
        # Get bounding box
        # x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y + h, x:x + w]
        # show ROI
        # cv2.imshow('segment no:'+str(i),roi)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # if w > 15 and h > 15:
        #     cv2.imwrite('out_check_out.png'.format(i), roi)

cv2.imshow('marked areas', image)
cv2.imwrite('out_check_out.png',image)
cv2.waitKey(0)