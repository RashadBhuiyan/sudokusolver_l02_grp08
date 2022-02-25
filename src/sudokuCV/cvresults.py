import numpy as np

## sudokuCV result class
class CVResults:
    def __init__(self, raw_results, confidence) -> None:
        self.raw_results = np.array(raw_results)
        self.confidence = np.array(confidence)

    ## returns indices of high and low confidences
    def getUnconfidentIndices(self, threshold):
        return (self.confidence < threshold).nonzero()[0]

    ## returns list of results with non-confident cells set to 0 (empty)
    def getConfidentResults(self, threshold):
        results = self.raw_results.copy()
        results[self.getUnconfidentIndices(threshold)] = 0
        return list(results)