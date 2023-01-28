from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/kontakt/')
def kontakt():
    return render_template('kontakt.html')

@app.route('/anleitung/')
def anleitung():
    return render_template('anleitung.html')

@app.route('/hintergrund/')
def hintergrund():
    return render_template('hintergrund.html')