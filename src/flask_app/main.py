from flask import Flask
from flask import render_template
from flask import request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/submit.html", methods = ["POST"])
def submit():
    image = request.files['formFile']
    return redirect("/")

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