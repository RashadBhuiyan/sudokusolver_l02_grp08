## Sudoku CV tester
from sudokucv import SudokuCV

# instantiates a cv object, do not instantiate multiple since loading model is slow
cv = SudokuCV("model/handwritten_printed.h5")

## can call recognize method as many times as needed, returns lists of results and confidence

print('\n====================================================\n')

result1 = cv.recognize("test_images/1.jpg", show_image = True)
if not result1.error:
    print(result1.getConfidentResults(0.75))
    print("Low recognition confidence in the following cells:", result1.getUnconfidentIndices(0.75))
else:
    print("ERROR:", result1.error)

print('\n====================================================\n')

result2 = cv.recognize("test_images/2.jpg")
if not result2.error:
    print(result2.getConfidentResults(0.75))
    print("Low recognition confidence in the following cells:", result2.getUnconfidentIndices(0.75))

    # testing image save/delete methods
    if result2.saveImg(''):
        print("Image successfully saved.")
        if result2.deleteImg(''):
            print("Image succesfully deleted")
        else:
            print("Image deletion failed!")
    else:
        print("Image save failed!")

else:
    print("ERROR:", result2.error)

print('\n====================================================\n')

result3 = cv.recognize("test_images/4.jpg")
if not result3.error:
    print(result3.getConfidentResults(0.75))
    print("Low recognition confidence in the following cells:", result3.getUnconfidentIndices(0.75))
else:
    print("ERROR:", result3.error)



