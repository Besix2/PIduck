from flask import Flask, render_template, request, redirect, url_for 
import sys
import subprocess

app = Flask(__name__)
sys.path.insert(0, "/")

@app.route('/')
def Home():
    return render_template("home.html")

@app.route('/scripts')
def scripts():
    return render_template('scripts.html')

@app.route('/settings')
def data():
    return render_template('settings.html')

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        text_value = str(request.form.get("text"))
        subprocess.run(["python", "/home/pi/PIduck/static_files/test.py", text_value], cwd="/home/pi/PIduck/static_files")
        return render_template("home.html")
if __name__ == '__main__':
    app.run(debug=True)