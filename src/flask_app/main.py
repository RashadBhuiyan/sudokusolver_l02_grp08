from flask import Flask
from flask import render_template
from flask import request, redirect
from solver import solve
from util import generateRandomValidBoard, isBoardValid, getSolvedCoordinates
from sudokucv.sudokucv import SudokuCV
import os
import json

app = Flask(__name__)
cv = SudokuCV(os.path.dirname(__file__) + "\\" + "\\sudokucv\\model\\handwritten_printed.h5")

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/upload")
def upload():
    return render_template("upload.html", error = "")

@app.route("/recognize", methods = ["POST"])
def recognize():
    # store the file in an image
    image = request.files['formFile'].read()

    # store the results of that model analysis
    results = cv.recognize(image, is_file=False)

    if (not results.error):
        board = results.getConfidentResults(0.75)
        confidence = results.getConfidence()
        image = results.getImage()
        return render_template("recognize.html", inputBoard=board, inputConfidence=confidence, inputImage=image)
    else:
        return render_template("upload.html", error=results.error)

@app.route("/solver", methods = ["POST"])
def solver():
    tableJSON = request.form.get('tableJSON')
    print(tableJSON)
    board = json.loads(tableJSON)
    solvedCoordinates = []
    getSolvedCoordinates(board, solvedCoordinates)
    success = solve(board)
    print("solve successful: ", success)
    return render_template("solution.html", solution=board, indices=solvedCoordinates, success=str(success))

@app.route("/manual")
def manual():
    return render_template("manual.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")
    
if __name__ == "__main__":
    app.run(debug=True)