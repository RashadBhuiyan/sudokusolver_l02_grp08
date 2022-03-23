from flask import Flask
from flask import render_template
from flask import request, redirect
from solver import solve_randomly, getSolvedCoordinates
from generator import generateRandomValidBoard
from sudokucv.sudokucv import SudokuCV
import os
import json

app = Flask(__name__)
cv = SudokuCV(os.path.dirname(__file__) + "\\" + "\\sudokucv\\model\\handwritten_printed.h5")

## load homepage of flask app
@app.route("/")
def home():
    return render_template("home.html")

## load upload page of flask app    
@app.route("/upload")
def upload():
    return render_template("upload.html", error = "")

## takes the Sudoku board and returns the best classification of it or an error
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

## takes the Sudoku board from the table, solves it, then renders the solutions page with it
@app.route("/solver", methods = ["POST"])
def solver():
    tableJSON = request.form.get('tableJSON')
    print(tableJSON)
    board = json.loads(tableJSON)
    solvedCoordinates = getSolvedCoordinates(board)
    success = solve_randomly(board)
    print("solve successful: ", success)
    return render_template("solution.html", solution=board, indices=solvedCoordinates, success=str(success))

## loads the manual input page for the flask app
@app.route("/manual")
def manual():
    return render_template("manual.html")

@app.route("/solver2", methods = ["POST"])
def solver2():
    tableJSON = request.form.get('tableJSON')
    print(tableJSON)
    board = json.loads(tableJSON)
    solvedCoordinates = getSolvedCoordinates(board)
    success = solve_randomly(board)
    print("solve successful: ", success)
    return render_template("solution2.html", solution=board, indices=solvedCoordinates, success=str(success))

## returns the play game page for the flask app (should have pencil function by revision 1)
@app.route("/game")
def game():
    return render_template("game.html")

## returns the game that the user can play
@app.route("/play", methods=["POST"])
def play():
    hints = request.form.get('hints')
    print(hints)
    board = generateRandomValidBoard(int(hints))
    givenCoordinates = getSolvedCoordinates(board)
    return render_template("play.html", gameBoard=board, indices=givenCoordinates)

@app.route("/solver3", methods = ["POST"])
def solver3():
    tableJSON = request.form.get('tableJSON')
    print(tableJSON)
    board = json.loads(tableJSON)
    solvedCoordinates = getSolvedCoordinates(board)
    success = solve_randomly(board)
    print("solve successful: ", success)
    return render_template("solution3.html", solution=board, indices=solvedCoordinates)

## returns the instructions page for the flask app (should be within gamepage by revision 1)
@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

## runs the flask app
if __name__ == "__main__":
    app.run(debug=True)