from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home/home.html')

@app.route('/home/kontakt/')
def kontakt():
    return render_template('home/kontakt.html')

@app.route('/home/anleitung/')
def anleitung():
    return render_template('home/anleitung.html')

@app.route('/home/hintergrund/')
def hintergrund():
    return render_template('home/hintergrund.html')

""" Level 1: Streming Abo beenden """
@app.route('/deceptv/')
def deceptv():
    return render_template('deceptv/deceptv.html')

@app.route('/deceptv/account/')
def deceptv_account():
    return render_template('deceptv/deceptv_account.html')

@app.route('/deceptv/angebote/')
def deceptv_angebote():
    return render_template('deceptv/deceptv_angebote.html')

@app.route('/deceptv/datenschutzmanager/')
def deceptv_datenschutzmanager():
    return render_template('deceptv/deceptv_datenschutzmanager.html')

@app.route('/deceptv/datenschutrichtlinie/')
def deceptv_datenschutzrichtlinie():
    return render_template('deceptv/deceptv_datenschutzrichtlinie.html')

@app.route('/deceptv/erkunden')
def deceptv_erkunden():
    return render_template('deceptv/deceptv_erkunden.html')

@app.route('/deceptv/premium/')
def deceptv_premium():
    return render_template('deceptv/deceptv_premium.html')

@app.route('/deceptv/favoriten/')
def deceptv_favoriten():
    return render_template('deceptv/deceptv_favoriten.html')

@app.route('/deceptv/feedback/')
def deceptv_feedback():
    return render_template('deceptv/deceptv_feedback.html')

@app.route('/deceptv/vorschlaege')
def deceptv_vorschlaege():
    return render_template('deceptv/deceptv_vorschlaege.html')

@app.route('/deceptv/impressum/')
def deceptv_impressum():
    return render_template('deceptv/deceptv_impressum.html')



if __name__ == "__Main__":
    app.run(debug=True)