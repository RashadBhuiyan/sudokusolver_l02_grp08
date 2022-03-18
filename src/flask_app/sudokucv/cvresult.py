import numpy as np
import cv2
import uuid
import os
import base64

## sudokuCV result class
class CVResult:
    def __init__(self, raw_results, confidence, image, error = '') -> None:
        self.raw_results = np.array(raw_results)
        self.confidence = np.array(confidence)
        self.error = error
        self.image = image
        self.uuid = uuid.uuid1()

    ## returns indices of high and low confidences
    def _getUnconfidentIndices(self, threshold):
        return (self.confidence < threshold).nonzero()[0]

    ## returns 2D list of results with non-confident cells set to 0 (empty)
    def getConfidentResults(self, threshold):
        results = self.raw_results.copy()
        results[self._getUnconfidentIndices(threshold)] = 0
        return results.reshape(9,9).tolist()

    ## returns 2D list of confidence values from 0 to 1
    def getConfidence(self):
        return self.confidence.reshape(9,9).tolist()

    ## saves the detected sudoku board as an image, returns path if successful
    def saveImg(self, directory):
        path = self._getFullImagePath(directory)
        if cv2.imwrite(path, self.image):
            return path

    def getImage(self):
        _, image = cv2.imencode('.png', self.image)
        return base64.b64encode(image).decode("UTF-8")

    ## removes previously generated image from path, returns path if successful
    def deleteImg(self, directory):
        path = self._getFullImagePath(directory)
        try: 
            os.remove(path)
            return path
        except: pass

    def _getFullImagePath(self, path):
        if path != '' and path[-1] != '/': 
            path += '/'
        path += self.uuid.hex + ".jpg"
        return path