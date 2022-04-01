import cv2
import numpy as np
from tensorflow.keras.models import load_model
from sudokucv.cvresult import CVResult
import sudokucv.cverrors as err

from PIL import Image, ExifTags
import io

class SudokuCV:
    WIDTH = 900
    HEIGHT = 900
    MIN_IMAGE_WIDTH = 200
    MIN_IMAGE_HEIGHT = 200

    ## initialize with model file path, show_image displays debug intermediary graphics
    def __init__(self, model_file) -> None:
        self.model = load_model(model_file)

    ## Preprocess image for board outline recognition
    def __preProcess(self, image):
        imgBlur = cv2.GaussianBlur(image, (5, 5), 1)
        imgThreshold = cv2.adaptiveThreshold( imgBlur, 255, 1, 1, 11, 2)
        return imgThreshold

    ## Split input image into list of cells
    def __getCells(self, image):
        cells = []
        rows = np.vsplit(image, 9)
        for row in rows:
            columns = np.hsplit(row, 9) 
            for col in columns:
                cells.append(col)
        return cells

    ## Attempt to identify number with Keras model
    def __getPrediction(self, cells):
        result = [0] * 81
        confidence = [0] * 81

        for i, cell in enumerate(cells):
            img = np.asarray(cell)
            img = img[10:img.shape[0] - 10, 10:img.shape[1] - 10]   # crop out grid borders
            img = cv2.resize(img, (28, 28))
            img = img / 255                                         # normalize
            # img = 1-img
            img = img.reshape(1, 28, 28, 1)                         # resize to match model shape

            predictions = self.model.predict(img)

            result[i] = np.argmax(predictions, axis=-1)[0]
            confidence[i] = np.amax(predictions)

        return (result, confidence)
        
    ## Returns the biggest contour and its area
    def __biggestContour(self, contours):
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
    def __getOrderedCorners(self, contour):
        midpoint = np.sum(contour, axis = 0)/4
        angles = - np.reshape(np.arctan2(contour[:,:,1] - midpoint[0,1], contour[:,:,0] - midpoint[0,0]), (1,4))
        contour = contour[(angles).argsort()]
        return contour

    def __removePerspective(self, image, corners):
        targetCorners = np.float32([[0, self.HEIGHT], [self.WIDTH, self.HEIGHT],
                    [self.WIDTH, 0], [0, 0]])

        matrix = cv2.getPerspectiveTransform(np.float32(np.reshape(corners, (4,2))), targetCorners)
        return cv2.warpPerspective(image, matrix, (self.WIDTH,self.HEIGHT))

    def __error(self, error):
        return CVResult(None, None, None, err.getErrorMessage(error))

    def __orientationCorrection(self, img):
        if 274 in img.getexif():                    # exif has orientation tag
            orientation = img.getexif()[274]
            if orientation == 3:
                img=img.rotate(180, expand=True)
            elif orientation == 6:
                img=img.rotate(270, expand=True)
            elif orientation == 8:
                img=img.rotate(90, expand=True)
        return np.array(img)

    ## performs recognition on an image and returns a result object. The input image can be a file or directly from HTTP request (is_file = False)
    def recognize(self, image, is_file = True,show_image = False):
        if is_file:
            img = self.__orientationCorrection(Image.open(image))
        else:
            img = self.__orientationCorrection(Image.open(io.BytesIO(image)))
        
        dimensions = img.shape
        if dimensions[0] < self.MIN_IMAGE_WIDTH or dimensions[1] < self.MIN_IMAGE_HEIGHT:
            return self.__error(err.ERR_IMG_TOO_SMALL)

        img = cv2.resize(img, (self.WIDTH, self.HEIGHT))

        # convert 16 bit images to 8 bit for cv processing
        if img.dtype == np.uint16:
            img = (img/256).astype('uint8')

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgThreshold = self.__preProcess(img)

        # find contours 

        imgContours = img.copy()
        imgBigContour = img.copy()
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

        # find biggest contour
        biggestCorners, maxArea = self.__biggestContour(contours)
        if len(biggestCorners) == 0:
            return self.__error(err.ERR_NO_GRID)
        elif maxArea < 63504:               # 324^2 = 9 * model size = 9 * 28
            return self.__error(err.ERR_GRID_TOO_SMALL)

        biggestCorners = self.__getOrderedCorners(biggestCorners)
        cv2.drawContours(imgBigContour, biggestCorners, -1, (255, 0, 0), 3)

        imgFlattened = self.__removePerspective(img, biggestCorners)
        t = cv2.adaptiveThreshold(imgFlattened, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 15)
        imgFlattened[t==255] = 255

        # split grid into cells
        cells = self.__getCells(imgFlattened)     # cv2.adaptiveThreshold( imgFlattened, 255, 1, 1, 11, cv2.THRESH_TOZERO_INV)

        results, confidence = self.__getPrediction(cells)

        if (show_image):
            cv2.imshow("input", img)
            cv2.imshow("threshold", imgThreshold)
            cv2.imshow("Contours", imgContours)
            cv2.imshow("DetectedGrid", imgBigContour)
            cv2.imshow("Flattened", imgFlattened)
            cv2.waitKey(0)

        return CVResult(results, confidence, cv2.resize(imgFlattened, (500, 500)))