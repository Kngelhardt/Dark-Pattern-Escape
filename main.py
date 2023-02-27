from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)

if __name__ == "__main__":
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
    # relevant, falls ich mit liste arbeite in sessions
    #session.modified = True
    

# Set the secret key to some random bytes.
app.secret_key = 'ba07947163bdb665ab81b575db5f22a60083e6737e739c0ed73efd78af4598c9'

###################################################################################
""" Reset der Session auf die initialen werte """
@app.route('/reset')
def reset_session():
    session['data_score'] = 100
    session['geld_score'] = 100
    # Countdown = 300 sekunden, also 5 minuten
    session['countdown'] = 300
    session['dp_score'] = 0
     # level_fortschritt: 0 = 0 Level beendet, 1 = Level 1 beendet, 2  = Level 2 beendet
    session['level_fortschritt'] = 0 
    session['warenkorb'] = [1, 2, 3]
    return '', 204

###################################################################################
""" Mainpage """
@app.route('/')
def home():
    #initialisierung der Werte für eine Session beim ersten Aufruf der Seite
    if "data_score" not in session:
        session['data_score'] = 100
        session['geld_score'] = 20
        # Countdown = 300 sekunden, also 5 minuten
        session['countdown'] = 300
        session['dp_score'] = 0
        # level_fortschritt: 0 = 0 Level beendet, 1 = Level 1 beendet, 2  = Level 2 beendet
        session['level_fortschritt'] = 0 
        session['warenkorb'] = [1, 2, 3]
    return render_template('home/home.html')

@app.route('/home/intro')
def home_intro():
    return render_template('home/intro.html', level_fortschritt = session['level_fortschritt'])

@app.route('/home/kontakt/')
def kontakt():
    return render_template('home/kontakt.html')

@app.route('/home/anleitung/')
def anleitung():
    return render_template('home/anleitung.html')

@app.route('/home/hintergrund/')
def hintergrund():
    return render_template('home/hintergrund.html')

###################################################################################
""" Level 1: Streming Abo beenden """

""" Funktion: Bilder aus dem static/images/deceptv Verzeichnis laden
    return: liste mit strings der Files inkl. Path """
def get_streaming_images():
    # bildverzeichnis mit BIldern für die Streamingseite
    image_dir = os.listdir('static/images/deceptv')
    # Return: Die Namen der Bilder als string inkliusive path, um sie einfach laden zu können
    return ['/static/images/deceptv/' +file for file in image_dir]

#Startseite
@app.route('/deceptv/')
def deceptv():
    # lade 
    deceptv_images = get_streaming_images()
    # Da mit list.pop() gearbeitet wird, muss eine Länge der Liste von 5*15 gewärleistet
    # sein um Fehlermeldungen zu vermeiden
    
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

@app.route('/deceptv/rückerstattung')
def deceptv_nicht():
    return render_template('deceptv/deceptv_nicht.html')

@app.route('/deceptv/wie-kuendigen')
def deceptv_wie_kuendigen():
    return render_template('deceptv/deceptv_wie_kuendigen.html')

#Mitgliedschaft beenden
@app.route('/deceptv/premium/mitgliedschaft')
def level1_beenden():
    session['dp_score'] = session['dp_score']+2
    deceptv_images = get_streaming_images()
    return render_template('deceptv/end/level1_beenden.html', deceptv_images = deceptv_images)

@app.route('/deceptv/premium/mitgliedschaft-beenden')
def level1_beenden2():
    session['dp_score'] = session['dp_score']+2
    return render_template('deceptv/end/level1_beenden2.html')

@app.route('/deceptv/mitgliedschaft-beenden')
def ende_lv1():
    if session['level_fortschritt'] == 2:
        return '', 204
    else:
        session['level_fortschritt'] = 1 
        return '', 204


###########################################################################################
# Level 2: Shopping
@app.route('/decepdive') 
def decepdive():
    return render_template('decepdive/decepdive.html')

@app.route('/decepdive_produkt1', methods=['POST', 'GET'])
def decepdive_produkt1():
    return render_template('decepdive/decepdive_produkt1.html')

@app.route('/decepdive_produkt2')
def decepdive_produkt2():
    return render_template('decepdive/decepdive_produkt2.html')

@app.route('/decepdive_produkt3')
def decepdive_produkt3():
    return render_template('decepdive/decepdive_produkt3.html')

@app.route('/decepdive_produkt4')
def decepdive_produkt4():
    return render_template('decepdive/decepdive_produkt4.html')

@app.route('/decepdive_produkt5')
def decepdive_produkt5():
    return render_template('decepdive/decepdive_produkt5.html')

@app.route('/decepdive/warenkorb')
def decepdive_warenkorb():
    return render_template('decepdive/decepdive_warenkorb.html')

@app.route('/decepdive/warenkorb/konto')
def decepdive_warenkorb2():
    return render_template('decepdive/decepdive_warenkorb2.html')

@app.route('/decepdive/warenkorb/Daten')
def decepdive_warenkorb3():
    return render_template('decepdive/decepdive_warenkorb3.html')

@app.route('/decepdive/warenkorb/Übersicht')
def decepdive_warenkorb4():
    return render_template('decepdive/decepdive_warenkorb4.html')

@app.route('/decepdive/beenden')
def ende_lv2():
    session['level_fortschritt'] = 2
    return '', 204

""" 
ajax replace div/element
flask 204 response
flask 200 json response
ersetzen des kontents
 """