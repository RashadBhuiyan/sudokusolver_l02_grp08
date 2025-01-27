from flask import Flask
from flask import render_template
from flask import request, redirect
from solver import solve_randomly, getUnfilledCoordinates, validateBoard
from generator import generateRandomValidBoard
from sudokucv.sudokucv import SudokuCV
import os
import json
import copy

print("Initializing...")

with open(os.path.dirname(__file__) + "/config.json") as cfg:
    configs = json.load(cfg)
print("Config loaded")

app = Flask(__name__)
cv = SudokuCV(os.path.dirname(__file__) + configs["model_path"])
print("CV recognition model loaded")
print("Initializing Complete")

## load homepage of flask app
@app.route("/")
def home():
    return render_template("home.html")

## load upload page of flask app    
@app.route("/upload", methods = ["GET", "POST"])
def upload():
    action = request.form.get('action')
    if action == None:      # default to display upload page
        return render_template("upload.html", action="", error = "", manualCropState=False)

    elif action == "recognize": # request is for recognition
        # store the file in an image
        image = request.files['formFile'].read()
        cropCoords = request.form.get('cropCoords')
        # check if manual crop enabled
        if cropCoords:
            cropCoords = json.loads(cropCoords)
        else:
            cropCoords = None

        # store the results of model analysis
        results = cv.recognize(image, is_file=False, crop_coords = cropCoords)

        if (not results.error):
            board = results.getConfidentResults(configs["confidence_cutoff"])
            confidence = results.getConfidence()
            image = results.getImage()
            return render_template("upload.html", action=action, inputBoard=board, inputConfidence=confidence, inputImage=image)
        else:
            return render_template("upload.html", error=results.error, manualCropState=True, image=image)

    elif action == "solve": # request is for recognized board solution
        error = ""
        tableJSON = request.form.get('tableJSON')
        board = json.loads(tableJSON)
        solvedCoordinates = getUnfilledCoordinates(board)
        success = validateBoard(board)
        if (not success):
            error = configs["errors"]["no_solution"]
        return render_template("upload.html", action=action, error=error, solution=board, indices=solvedCoordinates, success=str(success))

    elif action == "play":
        error = ""
        tableJSON = request.form.get('tableJSON')
        board = json.loads(tableJSON)
        emptyCells = getUnfilledCoordinates(board)
        if len(emptyCells) == 0:
            # all boxes already filled, can't play
            return render_template("upload.html", action="solve", error=configs["errors"]["no_space"], solution=board, indices=emptyCells, success=str(False))
        unsolvedboard = copy.deepcopy(board)
        success = validateBoard(board)
        if (not success):
            # board is unsolvable
            return render_template("upload.html", action="solve", error=configs["errors"]["no_solution"], solution=board, indices=emptyCells, success=str(success))
        # redirect to play if valid unfilled board
        return render_template("play.html", gameBoard=unsolvedboard, indices=emptyCells, difficulty="Uploaded")

## returns the play game page for the flask app (should have pencil function by revision 1)
@app.route("/game")
def game():
    return render_template("game.html")

## returns the game that the user can play
@app.route("/play", methods=["GET", "POST"])
def play():
    action = request.form.get("action") 

    if action == None:
        difficulty = request.form.get('difficulty')
        board = generateRandomValidBoard(configs["difficulties"][difficulty])
        emptyCells = getUnfilledCoordinates(board)
        return render_template("play.html", gameBoard=board, indices=emptyCells, difficulty=difficulty)

    else:
        difficulty = request.form.get('difficulty')
        tableJSON = request.form.get('tableJSON')
        time = request.form.get('time')
        board = json.loads(tableJSON)
        solvedCoordinates = getUnfilledCoordinates(board)
        success = (action == "submit") or solve_randomly(board)
        return render_template("success.html", action=action, solution=board, indices=solvedCoordinates, success=str(success), time=time, difficulty=difficulty)


## runs the flask app
if __name__ == "__main__":
    app.run(debug=True)