from flask import Flask, render_template
import os

app = Flask(__name__)

""" Mainpage """
@app.route('/')
def home():
    return render_template('home/home.html')

@app.route('/home/intro')
def home_intro():
    return render_template('home/intro.html')

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
#Startseite
@app.route('/deceptv/')
def deceptv():
    # bildverzeichnis mit BIldern für die Carrousels der Streamingseite
    image_dir = os.listdir('static/images/deceptv')
    # Die Namen der Bilder als string inkliusive path seichern um sie einfach laden zu können
    deceptv_images = ['/static/images/deceptv/' +file for file in image_dir]
    # Da mit list.pop() gearbeitet wird, muss eine gewisse Länge gewärleistet sein um Fehlermeldungen zu vermeiden
    while len(deceptv_images) <= 5*15:
        deceptv_images = deceptv_images + deceptv_images

    return render_template('deceptv/deceptv.html', deceptv_images = deceptv_images) 

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

@app.route('/deceptv/favoriten/')
def deceptv_favoriten():
    return render_template('deceptv/deceptv_favoriten.html')

@app.route('/deceptv/feedback/')
def deceptv_feedback():
    return render_template('deceptv/deceptv_feedback.html')

@app.route('/deceptv/impressum/')
def deceptv_impressum():
    return render_template('deceptv/deceptv_impressum.html')

@app.route('/deceptv/premium/')
def deceptv_premium():
    return render_template('deceptv/deceptv_premium.html')

@app.route('/deceptv/service/')
def deceptv_service():
    return render_template('deceptv/deceptv_service.html')

@app.route('/deceptv/shop/')
def deceptv_shop():
    return render_template('deceptv/deceptv_shop.html')
    
@app.route('/deceptv/social/')
def deceptv_social():
    return render_template('deceptv/deceptv_social.html')

@app.route('/deceptv/vorschlaege')
def deceptv_vorschlaege():
    return render_template('deceptv/deceptv_vorschlaege.html')

#Mitgliedschaft beenden
@app.route('/deceptv/premium/mein-abo')
def beenden1():
    return render_template('deceptv/end/beenden1.html')
    





if __name__ == "__Main__":
    app.run(debug=True)