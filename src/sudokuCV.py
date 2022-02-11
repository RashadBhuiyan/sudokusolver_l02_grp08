from cmath import pi
import cv2
from matplotlib.pyplot import contour
import numpy as np
import math

def preProcess(image):
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
    imgThreshold = cv2.adaptiveThreshold( imgBlur, 255, 1, 1, 11, 2)
    return imgThreshold

def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if area > max_area: #and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area

def getOrderedCorners(contour):
    midpoint = np.sum(contour, axis = 0)/4
    angles = - np.reshape(np.arctan2(contour[:,:,1] - midpoint[0,1], contour[:,:,0] - midpoint[0,0]), (1,4))
    contour = contour[(angles).argsort()]
    return contour

WIDTH = 540;
HEIGHT = 540;
imagePath = '1.jpg'

img = cv2.imread(imagePath)
img = cv2.resize(img, (WIDTH, HEIGHT))
imgThreshold = preProcess(img)

# find contours

imgContours = img.copy()
imgBigContour = img.copy()
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

# find biggest contour

biggest, maxArea = biggestContour(contours)
biggest = getOrderedCorners(biggest)
cv2.drawContours(imgBigContour, biggest, -1, (255, 0, 0), 3)
#cv2.polylines(imgBigContour, biggest, True, (255,0,0))

targetCorners = np.float32([[0, 540], [540, 540],
                       [540, 0], [0, 0]])
matrix = cv2.getPerspectiveTransform(np.float32(np.reshape(biggest, (4,2))), targetCorners)
ImgFlattened = img.copy()
ImgFlattened = cv2.warpPerspective(ImgFlattened, matrix, (540,540))

# split grid into cells

cells = []
rows = np.vsplit(ImgFlattened, 9)
for row in rows:
    columns = np.hsplit(row, 9)
    for col in columns:
        cells.append(col)

cv2.imshow("cell", cells[1])


cv2.imshow("input", img)
cv2.imshow("threshold", imgThreshold)
cv2.imshow("contours", imgContours)
cv2.imshow("biggest contour", imgBigContour)
cv2.imshow("Flattened", ImgFlattened)
cv2.waitKey(0)