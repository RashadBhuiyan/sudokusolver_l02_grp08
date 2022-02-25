import cv2
import numpy as np
from tensorflow.keras.models import load_model
from cvresults import CVResults
import cverrors as err

class SudokuCV:
    WIDTH = 900
    HEIGHT = 900
    MIN_IMAGE_WIDTH = 400
    MIN_IMAGE_HEIGHT = 400

    ## initialize with model file path, show_image displays debug intermediary graphics
    def __init__(self, model) -> None:
        self.model = load_model(model)

    ## Preprocess image for board outline recognition
    def preProcess(self, image):
        imgGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
        imgThreshold = cv2.adaptiveThreshold( imgBlur, 255, 1, 1, 11, 2)
        return imgThreshold

    ## Split input image into list of cells
    def getCells(self, image):
        cells = []
        rows = np.vsplit(image, 9)
        for row in rows:
            columns = np.hsplit(row, 9) 
            for col in columns:
                cells.append(col)
        return cells

    ## Attempt to identify number with Keras model
    def getPrediction(self, cells):
        result = [0] * 81
        confidence = [0] * 81

        for i, cell in enumerate(cells):
            img = np.asarray(cell)
            img = img[10:img.shape[0] - 10, 10:img.shape[1] - 10]   # crop out grid borders
            img = cv2.resize(img, (28, 28))
            img = img / 255                                         # normalize
            img = 1-img
            img = img.reshape(1, 28, 28, 1)                         # resize to match model shape

            predictions = self.model.predict(img)

            result[i] = np.argmax(predictions, axis=-1)[0]
            confidence[i] = np.amax(predictions)

        return (result, confidence)
        
    ## Returns the biggest contour and its area
    def biggestContour(self, contours):
        biggest = np.array([])
        max_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.1 * perimeter, closed = True)
                if area > max_area and len(approx) == 4:
                    biggest = approx
                    max_area = area
        return biggest, max_area

    ## Sorts given corner points clockwise from top left
    def getOrderedCorners(self, contour):
        midpoint = np.sum(contour, axis = 0)/4
        angles = - np.reshape(np.arctan2(contour[:,:,1] - midpoint[0,1], contour[:,:,0] - midpoint[0,0]), (1,4))
        contour = contour[(angles).argsort()]
        return contour

    def removePerspective(self, image, corners):
        targetCorners = np.float32([[0, self.HEIGHT], [self.WIDTH, self.HEIGHT],
                    [self.WIDTH, 0], [0, 0]])

        matrix = cv2.getPerspectiveTransform(np.float32(np.reshape(corners, (4,2))), targetCorners)
        return cv2.warpPerspective(image, matrix, (self.WIDTH,self.HEIGHT))

    def Error(self, error):
        return CVResults(None, None, None, err.getErrorMessage(error))

    def recognize(self, imagePath, show_image = False):
        img = cv2.imread(imagePath)
        dimensions = img.shape
        if dimensions[0] < self.MIN_IMAGE_WIDTH or dimensions[1] < self.MIN_IMAGE_HEIGHT:
            return self.Error(err.ERR_IMG_TOO_SMALL)

        img = cv2.resize(img, (self.WIDTH, self.HEIGHT))
        imgThreshold = self.preProcess(img)

        # find contours 

        imgContours = img.copy()
        imgBigContour = img.copy()
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

        # find biggest contour
        biggestCorners, maxArea = self.biggestContour(contours)
        if len(biggestCorners) == 0:
            return self.Error(err.ERR_NOGRID)
        elif maxArea < 104976:               # 324^2 = 9 * (model size + 2 * border size) = 9 * (28 + 2*4)
            return self.Error(err.ERR_GRID_TOO_SMALL)

        biggestCorners = self.getOrderedCorners(biggestCorners)
        cv2.drawContours(imgBigContour, biggestCorners, -1, (255, 0, 0), 3)

        imgFlattened = self.removePerspective(img, biggestCorners)
        imgFlattened = cv2.cvtColor(imgFlattened, cv2.COLOR_BGR2GRAY)
        imgFlattened = cv2.adaptiveThreshold( imgFlattened, 255, 1, 1, 11, cv2.THRESH_TOZERO_INV)
        # split grid into cells
        cells = self.getCells(imgFlattened)

        results, confidence = self.getPrediction(cells)

        if (show_image):
            cv2.imshow("input", img)
            cv2.imshow("threshold", imgThreshold)
            cv2.imshow("Contours", imgContours)
            cv2.imshow("DetectedGrid", imgBigContour)
            cv2.imshow("Flattened", imgFlattened)
            cv2.waitKey(0)

        return CVResults(results, confidence, 255 - imgFlattened)