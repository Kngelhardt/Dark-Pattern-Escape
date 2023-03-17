from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)

if __name__ == "__main__":
    # Activate debugging
    app.run(debug = True)

# Set the secret key to some random bytes.
app.secret_key = 'ba07947163bdb665ab81b575db5f22a60083e6737e739c0ed73efd78af4598c9'

###################################################################################
"""  Reset der Session auf die initialen werte """
@app.route('/initialize-session')
def initialize_session():
    #debugging##############################
    if session.get("data_score") is not None:
        print(
        'data: ', session['data_score'],'\n',
        'geld: ',session['geld_score'],'\n',
        'countdown: ',session['countdown'],'\n',
        'dp: ',session['dp_score'],'\n',
        'success: ',session['level_fortschritt'],'\n',
        'lv1_show: ',session['cookie_lv1_show'],'\n',
        'lv1_fin: ', session['cookie_lv1_fertig'],'\n',
        'lv2_fin: ',session['cookie_lv1_fertig'],'\n',
        'warenkorb: ',session['warenkorb'],'\n',
        session['data_score'],'\n',
        session['geld_score'],'\n',
        session['countdown'],'\n',
        session['dp_score'],'\n',
        'level_fortschritt',session['level_fortschritt'],'\n',
        session['cookie_lv1_show'],'\n',
        session['cookie_lv1_fertig'],'\n',
        session['cookie_lv2_fertig'],'\n',
        'warenkorb',session['warenkorb'],'\n',
        'spende', session['spende_lv2'], '\n',
        # Aufreigungen mit Cookiebannern und ob sie richtig gelöst wurden
        # 3 Mögliche Werte: None(nicht abgeschlossen), True, False
        # cookiebanner lv1: 
        'dp_cookiemanager_lv',session['dp_open_cookiemanager_lv1'],'\n',
        'dp_cookie_lv1',session['dp_cookie_lv1'],'\n',
        'dp_berechtiges_interesse_lv1',session['dp_berechtiges_interesse_lv1'],'\n',
        'dp_cookiemisdirection_lv1',session['dp_cookiemisdirection_lv1'] ,'\n',
        # level1
        'dp_roachmotel1',session['dp_roachmotel1'] ,'\n',
        'dp_misdirect_kuendigen',session['dp_misdirect_kuendigen'],'\n',
        'dp_trickquestion1',session['dp_trickquestion1'] ,'\n',
        'dp_shaming_lv1', session['dp_shaming_lv1'],'\n',
        'dp_roachmotel2',session['dp_roachmotel2'] ,'\n',
        #cookiebanner lv2:
        'dp_cookielv2_trickquestion',session['dp_cookielv2_trickquestion'],'\n',
        'dp_cookielv2_trickquestion2',session['dp_cookielv2_trickquestion2'],'\n',
        'dp_cookielv2_berechtigt', session['dp_cookielv2_berechtigt'],'\n',
        # level 2
        'dp_vergleich', session['dp_vergleich'],'\n',
        'dp_preticked_monatl', session['dp_preticked_monatl'],'\n',
        'dp_sneakinbasket', session['dp_sneakinbasket'],'\n',
        'dp_hiddennewsletter', session['dp_hiddennewsletter'],'\n',
        'dp_misdirect_login', session['dp_misdirect_login'],'\n',
        'dp_misdirect_konto_erstellen', session['dp_misdirect_konto_erstellen'],'\n',
        'dp_misdirect_spende', session['dp_misdirect_spende'],'\n'
        )

    ######## Scores #############################
    session['data_score'] = 100
    session['geld_score'] = 25
    # Countdown = 300 sekunden, also 5 minuten
    session['countdown'] = 300
    session['dp_score'] = 0
     # level_fortschritt: 0 = 0 Level beendet, 1 = Level 1 beendet, 2  = Level 2 beendet
    session['level_fortschritt'] = 0 
    # Definiert ob in Level 1 das Cookiebanner gezegt wird
    session['cookie_lv1_show'] = False
    # Definiert ob im jeweiligen Level das Cookiebanner abgeschlossen wurde
    session['cookie_lv1_fertig']= False
    session['cookie_lv2_fertig']= False
    # Gesamtsumme des Warenkorbs in Level 2
    session['warenkorb'] = 0
    # Ist eine Monatliche Bestellung oder einfache Bestellung ausgewählt
    session['bestellung_monatl'] = None
    # Wenn das Dark Pattern 'dp_misdirect_spende' falsch gelöst wurde werden 2€ dem Entbetrag hinzugefügt
    session['spende_lv2'] = 0.00
    # Aufreigungen mit Cookiebannern und ob sie richtig gelöst wurden
    # 3 Mögliche Werte: None(nicht abgeschlossen), True, False
    ######## cookiebanner lv1: ######################
    session['dp_open_cookiemanager_lv1']  = None
    session['dp_cookie_lv1']  = None
    session['dp_berechtiges_interesse_lv1']  = None
    session['dp_cookiemisdirection_lv1']  = None
    ######## level1 #################################
    session['dp_roachmotel1']  = None
    session['dp_misdirect_kuendigen']  = None
    session['dp_trickquestion1']  = None
    session['dp_shaming_lv1']  = None
    session['dp_roachmotel2'] = None
    ######### cookiebanner lv2: #####################
    session['dp_cookielv2_trickquestion']= None
    session['dp_cookielv2_trickquestion2']= None
    session['dp_cookielv2_berechtigt']= None
    ######### level 2 ###############################
    session['dp_vergleich']  = None
    session['dp_preticked_monatl'] = None
    session['dp_sneakinbasket'] = None 
    session['dp_hiddennewsletter'] = None
    session['dp_misdirect_login'] = None
    session['dp_misdirect_konto_erstellen'] = None
    session['dp_misdirect_spende'] = None


    return render_template('home/intro.html', level_fortschritt = session['level_fortschritt'])

@app.route('/change-session', methods=['GET', 'POST'])
def set_session_value():
    if request.method == "POST":

        # lade json
        session_data = request.json

        # get session key
        for session_key in session_data:
            print('input', session_key, session_data[session_key])
            # True und False werte werden als 1 und 0 
            # geschickt und müssen wieder zu boolean geändert werden
            if isinstance(session[session_key],bool):
                session[session_key] = bool(session_data[session_key])
                #debugging
                print('update bool',session_key, session[session_key])
            elif isinstance(session[session_key], int):
                session[session_key] = session[session_key] + session_data[session_key]
                #debugging
                print('update int', session_key, session[session_key])    
            else:
                session[session_key] = session_data[session_key]
                # debugging
                print('update', session_key, session[session_key])   
        return '', 204
    else:
        return '', 204

""" Upadate des timers """
@app.route('/update_timer', methods=['GET', 'POST'])
def update_timer():
    if request.method == "POST":
        # lade den gesendeten zeitstand
        zeit_state = request.get_json()
        # speicher den Wert in session
        session['countdown'] = zeit_state['object']
        print(zeit_state['object'])
        return '', 204
    else:
        return '', 204

###################################################################################
""" Mainpage """
@app.route('/')
def home():
    #initialisierung der Werte für eine Session, check if session is initialised
    if session.get("data_score") is None:
        initialize_session()
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

@app.route('/home/fragebogen/')
def fragebogen():
    return render_template('home/fragebogen.html')

###################################################################################
""" Level 1: Streming Abo beenden """

""" Funktion: Bilder aus dem static/images/deceptv Verzeichnis laden
    return: liste mit strings der Files inkl. Path """
def get_streaming_images():
    # bildverzeichnis mit BIldern für die Streamingseite
    image_dir = os.listdir('static/images/deceptv')
    # Return: Die Namen der Bilder als string inkliusive path, um sie einfach laden zu können
    return ['/static/images/deceptv/' +file for file in image_dir]

@app.route('/cookie_form_lv1', methods=['GET','POST'])
def cookie_form_lv1():
    if request.method == 'POST':
        # Cookiedialog beenden und nicht wieder anzeigen
        session['cookie_lv1_fertig'] = 1
        session['cookie_lv1_show'] = 0

        # Wenn das Opt-Out Cookie Dark Pattern noch nicht gelöst wurde, ehöhe dp_score 
        # für jedes richtige Opt-Out-Feld
        if session["dp_cookie_lv1"] is None:
            counter_richtig = 0
            if 'CookieStandort' in request.form:
                session['dp_score'] = session['dp_score'] + 1
                counter_richtig += 1
            if 'CookieIdent' in request.form:
                session['dp_score'] = session['dp_score'] + 1
                counter_richtig += 1
            if 'CookieDeviceSaves' in request.form:
                session['dp_score'] = session['dp_score'] + 1
                counter_richtig += 1
            if 'CookiePersonalisierung' in request.form:
                session['dp_score'] = session['dp_score'] + 1
                counter_richtig += 1
            if 'CookieTargeting' in request.form:
                session['dp_score'] = session['dp_score'] + 1
                counter_richtig += 1
            # Wenn alle richtig markiert, dark Pattern als richtig gelöst setzen
            if counter_richtig == 5:
                 session['dp_cookie_lv1'] = 1
            else:
                 session['dp_cookie_lv1'] = 0

        # Wenn Dark Pattern mit Opt-Out Dark Pattern noch nicht gelöst ist:
        if session["dp_berechtiges_interesse_lv1"] is None:
            # Wenn die Opt-Out checkboxes ausgeschalten wurden
            if 'cookie_berechtigt1' not in request.form and 'cookie_berechtigt2' not in request.form:
                session['dp_score'] = session['dp_score'] + 5
                session['dp_berechtiges_interesse_lv1'] = 1
            else:
                session['dp_berechtiges_interesse_lv1'] = 0
        
        # Wenn das "Misdirection" Dark Pattern noch nicht gelöst ist:
        if session['dp_cookiemisdirection_lv1'] is None:
            session['dp_cookiemisdirection_lv1'] = 1
            session['dp_score'] = session['dp_score'] +5

    return redirect(url_for('deceptv'))

#Startseite
@app.route('/deceptv/')
def deceptv():
    # wenn das Level schon abschlossen ist, soll es nicht noch einmal gespielt werden 
    # daher wird ein redirect zur levelübersicht vollführt
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    # Cookiebanner beim ersten aufrufen sichtbar machen, es wird nach dem beenden der 
    # können Banner-Aufgabe wieder versteckt
    if session["cookie_lv1_fertig"] is False:
        session['cookie_lv1_show'] = True
    # lade bilder aus dem static/images/deceptv ordner
    deceptv_images = get_streaming_images()
    # Da mit list.pop() gearbeitet wird, muss eine Länge der Liste von 5*15 gewärleistet
    # sein um Fehlermeldungen zu vermeiden 
    while len(deceptv_images) <= 5*15:
        deceptv_images = deceptv_images + deceptv_images

    return render_template('deceptv/deceptv.html', deceptv_images = deceptv_images) 

@app.route('/deceptv/account/')
def deceptv_account():
    # wenn das Level schon abschlossen ist, soll es nicht noch einmal gespielt werden 
    # können daher wird ein redirect zur levelübersicht vollführt
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_account.html')

@app.route('/deceptv/angebote/')
def deceptv_angebote():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_angebote.html')

@app.route('/deceptv/datenschutzmanager/')
def deceptv_datenschutzmanager():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_datenschutzmanager.html')

@app.route('/deceptv/datenschutrichtlinie/')
def deceptv_datenschutzrichtlinie():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_datenschutzrichtlinie.html')

@app.route('/deceptv/erkunden')
def deceptv_erkunden():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_erkunden.html')

@app.route('/deceptv/favoriten/')
def deceptv_favoriten():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_favoriten.html')

@app.route('/deceptv/feedback/')
def deceptv_feedback():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_feedback.html')

@app.route('/deceptv/impressum/')
def deceptv_impressum():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_impressum.html')

@app.route('/deceptv/premium/')
def deceptv_premium():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_premium.html')

@app.route('/deceptv/service/')
def deceptv_service():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_service.html')

@app.route('/deceptv/shop/')
def deceptv_shop():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_shop.html')
    
@app.route('/deceptv/social/')
def deceptv_social():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_social.html')

@app.route('/deceptv/vorschlaege')
def deceptv_vorschlaege():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_vorschlaege.html')

@app.route('/deceptv/rückerstattung')
def deceptv_nicht():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_nicht.html')

@app.route('/deceptv/wie-kuendigen')
def deceptv_wie_kuendigen():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_wie_kuendigen.html')

#Mitgliedschaft beenden
@app.route('/deceptv/premium/mitgliedschaft')
def level1_beenden():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    deceptv_images = get_streaming_images()
    return render_template('deceptv/end/level1_beenden.html', deceptv_images = deceptv_images)

@app.route('/deceptv/premium/mitgliedschaft-beenden')
def level1_beenden2():
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/end/level1_beenden2.html')

@app.route('/ende_lv1')
def level1_beendet():
    if session['level_fortschritt'] == 0:

        session['level_fortschritt'] = 1
        print(session['geld_score'], session['countdown'])
        # Wenn der Countdown abläuft ohne, dass das Abo beendet wird, verlieren
        # Spieler*innen das Geld für das Abo
        if session['countdown'] <= 0:
            session['geld_score'] = session['geld_score'] -10
            
            
        # Wenn cookiebanner nicht gelöst, setzte data_score runter, beende cookie_lv1
        # und stelle sicher das cokkie_banner_lv1 nicht angezeigt wird
        if session['cookie_lv1_fertig'] is False:
            session['data_score'] = session['data_score'] -40
            session['cookie_lv1_show'] = False
            session['cookie_lv1_fertig']= True

        # resert countdown für level 2
        session['countdown'] = 300
    
    return render_template('deceptv/end/level1_beendet.html')


###########################################################################################
# Level 2: Shopping
@app.route('/decepdive') 
def decepdive():
    #Zeige Cookibanner
    #if session["cookie_lv2_fertig"] is False:
    #    session['cookie_lv2_show'] = True

    # wenn das Level schon abschlossen ist, soll es nicht noch einmal gespielt werden 
    # können daher wird ein redirect zur levelübersicht vollführt
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive.html')

# Formverarbeitung für ein Dark Pattern in Level2 
# Das Form besteht aus preticked checkboxes, die unticked werden müssen
@app.route('/decepdive_cookies', methods=['GET','POST'])
def decepdive_cookies():
    if request.method == "POST":
        # Cookiebanner auf beendet setzten, damit es nicht mehr erscheint
        session['cookie_lv2_fertig']= True
        # checken ob dp shcn gelöst
        if session['dp_cookielv2_berechtigt'] is None:
            # abfrage ob die angekruezte checkbox ausgeschaltet wurde
            if 'interesse1' not in request.form and 'interesse2' not in request.form:
                # Wenn angekruezt, wird dp_score erhöht
                session['dp_score'] = session['dp_score'] +5
                # Dark Pattern als richtig gelöst markieren
                session['dp_cookielv2_berechtigt'] = 1
            else:
                # Wenn nicht angekruezt, wird data_score verringert
                session['data_score'] = session['data_score'] -10
                # Dark Pattern als flasch gelöst markieren
                session['dp_cookielv2_berechtigt'] = 0

    return render_template('decepdive/decepdive.html')

@app.route('/warenkorb', methods=['GET', 'POST'])
def add_warenkorb():
    if request.method == "POST":
        if 'bestellung' in request.form:
            # dp falsch gelöst. (Monatliche kosten vermeiden)
            if request.form['bestellung'] == 'bestellung_monatl':
                session['warenkorb'] = 9
                session['bestellung_monatl'] = True
                if session['dp_preticked_monatl'] is None:
                    session['dp_preticked_monatl'] = 0
            # dp richtig gelöst. (Monatliche kosten vermeiden)
            if request.form['bestellung'] == 'bestellung_einzel':
                # checken, ob es schon gelöst wurde. Nur wenn nicht: Punkte vergeben
                if session['dp_preticked_monatl'] is None:
                    session['dp_score'] = session['dp_score'] + 5
                    session['dp_preticked_monatl'] = 1
                session['bestellung_monatl'] = False
                session['warenkorb'] = 9.99

   # direct zu warenkorb (nächste seite)
    return render_template('decepdive/decepdive_warenkorb.html')

@app.route('/konto_warenkorb', methods=['GET', 'POST'])
def agb_warenkorb():
    if request.method == "POST":
        # Error vermeiden
        if 'preis' in request.form:
            session['warenkorb'] = request.form['preis']
        # Wenn newslestter nicht abgelehnt: ziehe daten ab, 
        # Wenn abgelehnt: erhöhe dark pattern score
        if 'newsletter' in request.form:
            if request.form['newsletter'] == 'selected':
                # mehrfaches lösen verhindern
                if  session["dp_hiddennewsletter"] is None:
                    session['data_score'] = session['data_score']-10
                    session['dp_hiddennewsletter'] = 0
            elif request.form['newsletter'] == 'abgelehnt':
                # mehrfaches lösen verhindern
                if  session["dp_hiddennewsletter"] is None:
                    session['dp_score'] = session['dp_score'] + 5
                    session['dp_hiddennewsletter'] = 1
   # direct zu warenkorb2 (nächste seite)
    return render_template('decepdive/decepdive_warenkorb2.html')
 
@app.route('/decepdive_produkt1')
def decepdive_produkt1():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt1.html')

@app.route('/decepdive_produkt2')
def decepdive_produkt2():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt2.html')

@app.route('/decepdive_produkt3')
def decepdive_produkt3():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt3.html')

@app.route('/decepdive_produkt4')
def decepdive_produkt4():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt4.html')

@app.route('/decepdive_produkt5')
def decepdive_produkt5():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt5.html')

@app.route('/decepdive_produkt6')
def decepdive_produkt6():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt6.html')

@app.route('/decepdive_produkt7')
def decepdive_produkt7():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt7.html')

@app.route('/decepdive_produkt8')
def decepdive_produkt8():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt8.html')


@app.route('/decepdive/warenkorb')
def decepdive_warenkorb():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb.html')

@app.route('/decepdive/warenkorb/konto')
def decepdive_warenkorb2():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb2.html')

@app.route('/decepdive/warenkorb/Daten')
def decepdive_warenkorb3():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb3.html')

@app.route('/decepdive/warenkorb/Übersicht')
def decepdive_warenkorb4():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb4.html')


@app.route('/decepdive/warenkorb/zahlen')
def decepdive_warenkorb5():
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb5.html')

@app.route('/decepdive/ende_lv2')
def ende_lv2():
    # Setze levle_fortschritt auf null und leite damit den Abschluss des Spiels ein
    session['level_fortschritt'] = 2

    # Wenn der Countdown abgelaufen ist, wird als Strafe der 'Geld Score' runtergesetzt
    if session['countdown'] <= 0:
        # Wenn noch gar nichts im Warenkorb ist
        if session['warenkorb'] == 0:
            # Ziehe den in Levle 2 maximal möglichen Betrag (wie wenn alle DP's falsch gelöst wurden) ab
            session['geld_score'] = session['geld_score'] - 16.97
        # Sonst: ziehe den momentanen Warenkorb vom 'Geld Score' ab
        else:
            session['geld_score'] = session['geld_score'] - (session['warenkorb']+ session['spende_lv2'])

    # Wenn das DP 'bestellung_monatl' falsch (oder nicht) gelöst wurde, ziehe 9,00€ vom 
    # 'Geld Score' ab, so als würde es in einem Monat dann überraschend noch einmal geliefert
    if session['dp_preticked_monatl'] == 0 or session['dp_preticked_monatl'] is None:
        session['geld_score'] = session['geld_score'] - 9
    
    # Geld Score kann nich unter 0 sein:
    if session['geld_score'] < 0:
        session['geld_score'] = 0

    # Wenn cookiebanner nicht gelöst, setzte data_score runter, beende cookie_lv2
    # und stelle sicher das cokkie_banner_lv2 nicht angezeigt wird
    if session['cookie_lv2_fertig'] is False:
        session['data_score'] = session['data_score'] -40
        session['cookie_lv2_fertig']= True

    return render_template('decepdive/ende_lv2.html')
