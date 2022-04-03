from flask import Flask
from flask import render_template
from flask import request, redirect
from solver import solve, solve_randomly, getSolvedCoordinates
from generator import generateRandomValidBoard
from sudokucv.sudokucv import SudokuCV
import os
import json

app = Flask(__name__)
cv = SudokuCV(os.path.dirname(__file__) + "/sudokucv/model/handwritten_printed.h5")

## load homepage of flask app
@app.route("/")
def home():
    return render_template("home.html")

## load upload page of flask app    
@app.route("/upload", methods = ["GET", "POST"])
def upload():
    action = request.form.get('action')
    if action == None:      # default to display upload page
        return render_template("upload.html", error = "", manualCropState=False)

    elif action == "recognize": # request is for recognition
        # store the file in an image
        image = request.files['formFile'].read()
        cropCoords = request.form.get('cropCoords')
        # check if manual crop enabled
        if cropCoords:
            cropCoords = json.loads(cropCoords)
        else:
            cropCoords = None

        # store the results of that model analysis
        results = cv.recognize(image, is_file=False, crop_coords = cropCoords)

        if (not results.error):
            board = results.getConfidentResults(0.75)
            confidence = results.getConfidence()
            image = results.getImage()
            return render_template("upload.html", action=action, inputBoard=board, inputConfidence=confidence, inputImage=image)
        else:
            return render_template("upload.html", error=results.error, manualCropState=True, image=image)

    elif action == "solve": # request is for recognized board solution
        error = ""
        tableJSON = request.form.get('tableJSON')
        board = json.loads(tableJSON)
        solvedCoordinates = getSolvedCoordinates(board)
        success = solve_randomly(board)
        if (not success):
            error = "The solver was unable to produce a solution for your puzzle. Please check the supplied input digits for correctness."
        return render_template("upload.html", action=action, error=error, solution=board, indices=solvedCoordinates, success=str(success))


## loads the manual input page for the flask app
@app.route("/manual", methods = ["GET", "POST"])
def manual():
    action = request.form.get('action')

    if action == None:
        return render_template("manual.html")   # default to display manual page

    # check if table can be solved
    elif action == "solve":
        error = ""
        tableJSON = request.form.get('tableJSON')
        board = json.loads(tableJSON)
        solvedCoordinates = getSolvedCoordinates(board)
        success = solve_randomly(board)
        if (not success):
            error = "The solver was unable to produce a solution for your puzzle. Please check the supplied input digits for correctness."
        return render_template("manual.html", action=action, error=error, solution=board, indices=solvedCoordinates, success=str(success))

## returns the play game page for the flask app (should have pencil function by revision 1)
@app.route("/game")
def game():
    return render_template("game.html")

## returns the game that the user can play
@app.route("/play", methods=["GET", "POST"])
def play():
    action = request.form.get("action") 

    if action == None:
        hints = request.form.get('hints')
        board = generateRandomValidBoard(int(hints))
        givenCoordinates = getSolvedCoordinates(board)
        return render_template("play.html", gameBoard=board, indices=givenCoordinates)

    elif action == "solve":
        tableJSON = request.form.get('tableJSON2')
        board = json.loads(tableJSON)
        solvedCoordinates = getSolvedCoordinates(board)
        success = solve_randomly(board)
        return render_template("success.html", action=action, solution=board, indices=solvedCoordinates, success=str(success))
    
    elif action == "submit":
        tableJSON = request.form.get('tableJSON')
        time = request.form.get('time')
        board = json.loads(tableJSON)
        solvedCoordinates = getSolvedCoordinates(board)
        return render_template("success.html", action=action, solution=board, indices=solvedCoordinates, success="True", time=time)

## runs the flask app
if __name__ == "__main__":
    app.run(debug=True)