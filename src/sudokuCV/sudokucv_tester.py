## Sudoku CV tester
from sudokucv import SudokuCV
from cvresults import CVResults

# instantiates a cv object, do not instantiate multiple since loading model is slow
cv = SudokuCV("model/handwritten_printed.h5")

## can call recognize method as many times as needed, returns lists of results and confidence
# TODO: add error handling (fails to detect grid in 1.jpg)

# result1 = cv.recognize("test_images/1.jpg", show_image = True)
# print(result1.getConfidentResults(0.75))
# print("Low recognition confidence in the following cells:", result1.getUnconfidentIndices(0.75))

result2 = cv.recognize("test_images/2.jpg")
print(result2.getConfidentResults(0.75))
print("Low recognition confidence in the following cells:", result2.getUnconfidentIndices(0.75))

result3 = cv.recognize("test_images/4.jpg")
print(result3.getConfidentResults(0.75))
print("Low recognition confidence in the following cells:", result3.getUnconfidentIndices(0.75))



