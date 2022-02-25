from flask import Flask
from flask import render_template
from flask import request, redirect
from solver import solve
from util import convertInput, generateRandomValidBoard, isBoardValid
from sudokucv.sudokucv import SudokuCV

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/submit.html", methods = ["POST"])
def submit():
    # store the file in an image
    image = request.files['formFile'].read()

    # create a CV model that will analyze the image
    cv = SudokuCV("sudokucv/model/handwritten_printed.h5")

    # store the results of that model analysis
    results = cv.recognize(image, is_file=False)

    # store the board and solve it
    bo = results.raw_results
    bo = convertInput(bo)
    solve(bo)

    return render_template("upload.html", solvedBoard=bo)

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