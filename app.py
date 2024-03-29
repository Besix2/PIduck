from flask import Flask, render_template, request, redirect, url_for 
import sys
import subprocess
import socket

app = Flask(__name__)
sys.path.insert(0, "/")

@app.route('/')
def Home():
    return render_template("home.html")

@app.route('/scripts')
def Scripts():
    return render_template('scripts.html')

@app.route('/settings')
def Settings():
    return render_template('settings.html')

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        text_value = str(request.form.get("text"))
        text_value = text_value.replace("\r", "")
        subprocess.run(["sudo", "python", "test.py", text_value], cwd="static_files")
        return redirect(url_for("Home"))
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    app.run(host=s.getsockname()[0])
