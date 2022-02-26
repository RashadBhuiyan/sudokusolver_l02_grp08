from flask import Flask
from flask import render_template
from flask import request, redirect
from solver import solve
from util import convertInput, generateRandomValidBoard, isBoardValid
from sudokucv.sudokucv import SudokuCV
import os

app = Flask(__name__)
cv = SudokuCV(os.path.dirname(__file__) + "\\" + "\\sudokucv\\model\\handwritten_printed.h5")

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/upload")
def upload():
    return render_template("upload.html", empty=True)

@app.route("/solve.html", methods = ["POST"])
def solveroute():
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for row in range(9):
        for column in range(9):
            value = request.form.get(str(row) + "," + str(column))
            board[row][column] = int(value) if value != "" else 0

    solve(board)
    return render_template("upload.html", solvedBoard=board)

@app.route("/submit.html", methods = ["POST"])
def submit():
    # store the file in an image
    image = request.files['formFile'].read()

    # store the results of that model analysis
    results = cv.recognize(image, is_file=False)

    # store the board and solve it
    bo = results.getConfidentResults(0.75)
    convertedBo = convertInput(bo)
    # solve(convertedBo)

    return render_template("upload.html", solvedBoard=convertedBo)

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