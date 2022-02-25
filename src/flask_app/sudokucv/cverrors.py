ERR_NOGRID = 0
ERR_EMPTY = 1
ERR_GRID_TOO_SMALL = 2
ERR_IMG_TOO_SMALL = 3


messages = {
    ERR_NOGRID: "No Sudoku grid is detected in this image. Ensure adequate lighting and frontal angle to improve detection.",
    ERR_EMPTY: "No digits were detectable on the Sudoku image.",
    ERR_GRID_TOO_SMALL: "The detected Sudoku grid appears too small for recognition. Take a closer picture.",
    ERR_IMG_TOO_SMALL: "The input image is too small. Submit a higher resolution picture."
}

def getErrorMessage(error):
    return messages[error]