from flask import Flask, render_template, request, redirect, session, url_for
import os
import csv

app = Flask(__name__)

# initialisiere secret key
app.secret_key = 'ba07947163bdb665ab81b575db5f22a60083e6737e739c0ed73efd78af4598c9'
  
########################### Request Funktionen ###################################
"""  Funktion initialisiert Standardwerte der Session, falls noch sie nicht initialisiert sind"""
@app.route('/initialize-session')
def initialize_session():
    # Initialisiere Session Werte
    # Nur beim ersten aufrufen der Seite ausführen
    if session.get('session_id') is None:

        # Initialisiere ID
        session['session_id'] = 1
        # erstelle liste mit allen vergebenen IDs
        id_list = []
        # check ob datei existiert, wenn ja öffnen zum lesen
        if os.path.isfile('ergebnisse/id_list.csv'):
            with open('ergebnisse/id_list.csv', 'r') as id_csv:
                reader = csv.reader(id_csv)
                # Füge verhandene IDs zu id_list hinzu
                for col in reader:
                    id_list.append(col[0])
        # falls die generierte id schon existiert, erhöhe ID um 1 bis ID einzigartig ist
        while str(session['session_id']) in id_list:
            session['session_id'] += 1
        # speicher id in id_csv, damit sie nicht doppelt vergeben werden kann
        with open('ergebnisse/id_list.csv', 'a') as id_csv:
            writer = csv.writer(id_csv)
            writer.writerow([session['session_id']])

        # initiale Werte der Punkte
        session['data_score'] = 100
        session['geld_score'] = 25
        session['dp_score'] = 0
        # Countdown = 300 sekunden, also 5 minuten (pro level)
        session['countdown'] = 300
        # level_fortschritt: 0 = 0 Level beendet, 1 = Level 1 beendet, 2  = Level 2 beendet
        session['level_fortschritt'] = 0 
        # Definiert ob in Level 1 das Cookiebanner und Nagging-Dialog gezegt wird
        session['cookie_lv1_show'] = False
        session['show_nagging']= True
        # Definiert ob im jeweiligen Level das Cookiebanner abgeschlossen wurde
        session['cookie_lv1_fertig']= None
        session['cookie_lv2_fertig']= None
        # Gesamtsumme des Warenkorbs in Level 2
        session['warenkorb'] = 0
        # Ist eine Monatliche Bestellung oder einfache Bestellung ausgewählt
        session['bestellung_monatl'] = None
        # Wenn das Dark Pattern 'dp_misdirect_spende' falsch gelöst wurde werden 2€ dem Entbetrag hinzugefügt
        session['spende_lv2'] = 0.00
        # Werte der jeweiligen Dark Patterns 
        # 3 Mögliche Werte: None(nicht abgeschlossen), 1(richt gelöst), 0(falsch gelöst)
        # cookiebanner lv1: 
        session['dp_open_cookiemanager_lv1']  = None
        session['dp_cookie_lv1']  = None
        session['dp_berechtiges_interesse_lv1']  = None
        session['dp_cookiemisdirection_lv1']  = None
        # level1 
        session['dp_nagging_level1'] = None
        session['dp_roachmotel1']  = None
        session['dp_misdirect_kuendigen']  = None
        session['dp_trickquestion1']  = None
        session['dp_shaming_lv1']  = None
        session['dp_roachmotel2'] = None
        # cookiebanner lv2:
        session['dp_cookielv2_trickquestion']= None
        session['dp_cookielv2_trickquestion2']= None
        session['dp_cookielv2_berechtigt']= None
        # level 2 
        session['dp_vergleich']  = None
        session['dp_preticked_monatl'] = None
        session['dp_sneakinbasket'] = None 
        session['dp_hiddennewsletter'] = None
        session['dp_misdirect_login'] = None
        session['dp_misdirect_konto_erstellen'] = None
        session['dp_misdirect_spende'] = None

    return render_template('home/intro.html', level_fortschritt = session['level_fortschritt'])

""" Funktion mit der Sessionwerte geändert werden können """
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
            # bei int werten soll es auf den momentanten Wert der Session aufaddiert werden
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


""" Upadate des timers in den Levels """
@app.route('/update_timer', methods=['GET', 'POST'])
def update_timer():
    if request.method == "POST":
        # lade den gesendeten zeitstand
        zeit_state = request.get_json()
        # speicher den Wert in session
        session['countdown'] = zeit_state['object']
        return '', 204
    else:
        return '', 204
    
###################################### HOMEPAGE ROUTES ############################################
""" Mainpage """
@app.route('/')
def home():
    # initialisierung der Werte für die Session
    initialize_session()
    return render_template('home/home.html')

@app.route('/home/uebersicht')
def home_intro():
    initialize_session()
    return render_template('home/intro.html', level_fortschritt = session['level_fortschritt'])

@app.route('/home/anleitung/')
def anleitung():
    initialize_session()
    return render_template('home/anleitung.html')


################################## LEVEL 1: Streaming Abo beenden ##################################

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
        # Kombination aus 2 Dark Patterns: Misdirection- (Aufmerksamkeit von relevanten Inhalten ablenken)
        # und Trickquestion Dark Pattern (Ja-Nein Antwort bezieht sich auch Ablenen, anstatt wie gewöhlich auf Annhemen)
        # für jedes richtige Opt-In-to-Opt-Out Feld: ehrhöhe den DP,Score, für jedes falsche: ziehe 4 Datenpunkte ab
        counter_richtig = 0
        if 'CookieStandort' in request.form:
            counter_richtig += 1
        if 'CookieIdent' in request.form:
            counter_richtig += 1
        if 'CookieDeviceSaves' in request.form:
            counter_richtig += 1
        if 'CookiePersonalisierung' in request.form:
            counter_richtig += 1
        if 'CookieTargeting' in request.form:
            counter_richtig += 1
            print('counter_richtig', counter_richtig)
        # Wenn alle Cookiezustimmungen entfernt wurden
        if counter_richtig == 5:
            # Wenn Dark Pattern noch nicht gelöst, als Pattern als richtig gelöst setzen und Punkte erhöhen
            if session["dp_cookie_lv1"] is None:
                session['dp_cookie_lv1'] = 1
                session['dp_score'] = session['dp_score'] + counter_richtig
                print('in dp: ', session['data_score'] )
            # Wenn es versäumt wurde, dan Cookiedialog richtig zu öffnen (-> -40 "data_score"), gibt es die
            # Chance die Datenpunkte wieder zurückzubekommen, wenn Dialog über die seite "Datenschutz-Manager"
            # geöffnet wurde
            elif session['dp_cookie_lv1'] == 0:
                session['data_score'] = session['data_score'] + (counter_richtig*4)
                print('not in dp: ', session['data_score'])
        # Punkte nur abziehen, falls data Score noch bei 100, damit ein erneutes aufrufen des Cookie-Managers
        # nicht bestraft werden kann, sondern nur belohnt
        else:
            if session['data_score'] == 100:
                session['data_score'] = session['data_score'] - (20 -counter_richtig*4)
                print('akzeptiert: ', session['data_score'])
            if session["dp_cookie_lv1"] is None:
                session['dp_cookie_lv1'] = 0
            

        # Wenn Dark Pattern mit Opt-Out Dark Pattern noch nicht gelöst ist:
        if session["dp_berechtiges_interesse_lv1"] is None:
            # Wenn die Opt-Out checkboxes ausgeschalten wurden
            if 'cookie_berechtigt1' not in request.form and 'cookie_berechtigt2' not in request.form:
                session['dp_score'] = session['dp_score'] + 5
                session['dp_berechtiges_interesse_lv1'] = 1
            else: 
                session['dp_berechtiges_interesse_lv1'] = 0 
                session['data_score'] = session['data_score'] -20
                print('akzeptiert berecht: ', session['data_score'])
        # Wenn es versäumt wurde, dan Cookiedialog richtig zu öffnen (-> -40 "data_score"), gibt es eine
        # Chance die Datenpunkte wieder zurückzubekommen, wenn Dialog über die seite "Datenschutz-Manager"
        # geöffnet wurde
        if session["dp_berechtiges_interesse_lv1"] == 0:
            if 'cookie_berechtigt1' not in request.form and 'cookie_berechtigt2' not in request.form:
                session['data_score'] = session['data_score'] +20
        
        # Wenn das "Misdirection" Dark Pattern ("Auswahl bestätigen" ist schlicht, "Akzeptieren" ist auffallend) noch nicht gelöst ist:
        if session['dp_cookiemisdirection_lv1'] is None:
            session['dp_cookiemisdirection_lv1'] = 1
            session['dp_score'] = session['dp_score'] +5
        
        # Sicherung, dass durch Fehler data_score nicht über 100 Sein kann
        if session['data_score'] > 100:
            session['data_score'] = 100

    return redirect(url_for('deceptv'))

#Startseite
@app.route('/deceptv/')
def deceptv():
    initialize_session()
    print('start: ', session['dp_score'])
    # wenn das Level schon abschlossen ist, soll es nicht noch einmal gespielt werden 
    # daher wird ein redirect zur levelübersicht vollführt
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    # Cookiebanner beim ersten aufrufen sichtbar machen, es wird nach dem beenden der 
    # können Banner-Aufgabe wieder versteckt
    if session["cookie_lv1_fertig"] is None:
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
    initialize_session()
    # wenn das Level schon abschlossen ist, soll es nicht noch einmal gespielt werden 
    # können daher wird ein redirect zur levelübersicht vollführt
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_account.html')

@app.route('/deceptv/angebote/')
def deceptv_angebote():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_angebote.html')

@app.route('/deceptv/datenschutzmanager/')
def deceptv_datenschutzmanager():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_datenschutzmanager.html')

@app.route('/deceptv/datenschutrichtlinie/')
def deceptv_datenschutzrichtlinie():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_datenschutzrichtlinie.html')

@app.route('/deceptv/erkunden')
def deceptv_erkunden():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_erkunden.html')

@app.route('/deceptv/favoriten/')
def deceptv_favoriten():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    
    deceptv_images = get_streaming_images()
    while len(deceptv_images) <= 5*15:
        deceptv_images = deceptv_images + deceptv_images

    return render_template('deceptv/deceptv_favoriten.html', deceptv_images=deceptv_images)

@app.route('/deceptv/feedback/')
def deceptv_feedback():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_feedback.html')

@app.route('/deceptv/premium/')
def deceptv_premium():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_premium.html')

@app.route('/deceptv/service/')
def deceptv_service():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_service.html')

@app.route('/deceptv/shop/')
def deceptv_shop():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_shop.html')
    
@app.route('/deceptv/social/')
def deceptv_social():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_social.html')

@app.route('/deceptv/vorschlaege')
def deceptv_vorschlaege():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    
    deceptv_images = get_streaming_images()
    while len(deceptv_images) <= 5*15:
        deceptv_images = deceptv_images + deceptv_images

    return render_template('deceptv/deceptv_vorschlaege.html', deceptv_images=deceptv_images)

@app.route('/deceptv/rückerstattung')
def deceptv_nicht():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_nicht.html')

@app.route('/deceptv/wie-kuendigen')
def deceptv_wie_kuendigen():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/deceptv_wie_kuendigen.html')

#Mitgliedschaft beenden
@app.route('/deceptv/premium/mitgliedschaft')
def level1_beenden():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    deceptv_images = get_streaming_images()
    return render_template('deceptv/end/level1_beenden.html', deceptv_images = deceptv_images)

@app.route('/deceptv/premium/mitgliedschaft-beenden')
def level1_beenden2():
    initialize_session()
    if session['level_fortschritt'] >= 1:
        return redirect(url_for('home_intro'))
    return render_template('deceptv/end/level1_beenden2.html')

@app.route('/ende_lv1')
def level1_beendet():
    initialize_session()
    # updates nur, falls Level noch nicht beendet war, damit updates nicht zwei mal durchgeführt werden können
    if session['level_fortschritt'] == 0:
        session['level_fortschritt'] = 1
        # Wenn der Countdown abläuft ohne, dass das Abo beendet wird, verlieren
        # Spieler*innen das Geld für das Abo
        if session['countdown'] <= 0:
            session['geld_score'] = session['geld_score'] -10
            session['abo_beendet']= False
        else:
            session['abo_beendet']= True
        # resert countdown für level 2
        session['countdown'] = 300
        
    # Wenn cookiebanner nicht gelöst, setzte data_score runter, beende cookie_lv1
    # und stelle sicher das cokkie_banner_lv1 nicht angezeigt wird
    if session['cookie_lv1_fertig'] is None:
        session['data_score'] = session['data_score'] -40
        session['cookie_lv1_show'] = False
        session['cookie_lv1_fertig']= True

    # Wenn im Naggingdialog nie auf "APP installieren" gedrückt wurde erhöhe dp_score um 5 und markiere dp als gelöst
    if  session['dp_nagging_level1'] is None:
        # Dark Pattern als richtig gelöst setzen
        session['dp_nagging_level1'] = 1
        # DP-Score erhöhrn
        session['dp_score'] = session['dp_score'] +5
    #Nagging-Fenster nicht merh anzeigen
    session['show_nagging'] = False
    
    dp_list_lv1 = [ session['dp_open_cookiemanager_lv1'],
                    session['dp_cookie_lv1'],
                    session['dp_berechtiges_interesse_lv1'],
                    session['dp_cookiemisdirection_lv1'],
                    session['dp_nagging_level1'],
                    session['dp_roachmotel1'],
                    session['dp_misdirect_kuendigen'],
                    session['dp_trickquestion1'],
                    session['dp_shaming_lv1'],
                    session['dp_roachmotel2'] ]
    print(dp_list_lv1)
    
    return render_template('deceptv/end/ende_lv1.html', dp_list_lv1 = dp_list_lv1)


############################ Level 2: Shopping ############################################
# Starseite
@app.route('/decepdive') 
def decepdive():
    initialize_session()
    #Zeige Cookibanner
    #if session["cookie_lv2_fertig"] is False:
    #    session['cookie_lv2_show'] = True

    # wenn das Level schon abschlossen ist, soll es nicht noch einmal gespielt werden 
    # können daher wird ein redirect zur levelübersicht vollführt
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive.html')

# Formverarbeitung für ein Dark Pattern in Level2 
# Das Form besteht aus vorangekreutzen Checkboxen, bei denen das Kreuz entfernt werden muss
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
        # error vermeiden: check, ob input vorhanden
        if 'bestellung' in request.form:
            # dp_preticked_monatl falsch gelöst. (Monatliche kosten vermeiden): als flasch(0) setzen
            if request.form['bestellung'] == 'bestellung_monatl':
                session['warenkorb'] = 9
                session['bestellung_monatl'] = True
                if session['dp_preticked_monatl'] is None:
                    session['dp_preticked_monatl'] = 0
            # dp richtig gelöst: als gelöst(1) setzten
            elif request.form['bestellung'] == 'bestellung_einzel':
                # checken, ob es schon gelöst wurde. Nur wenn nicht: Punkte vergeben
                if session['dp_preticked_monatl'] is None:
                    session['dp_score'] = session['dp_score'] + 5
                    # dark pattern als gelöst(1) setzen
                    session['dp_preticked_monatl'] = 1
                session['bestellung_monatl'] = False
                session['warenkorb'] = 9.99
            # dp_vergleich falsch gelöst: als flasch(0) setzen
            if request.form['dp_vergleich'] == 'teurer':
                # nur änder, wenn noch nicht gelöst (None)
                if session['dp_vergleich'] is None:
                    session['dp_vergleich'] = 0
            # dp_vergleich richtig gelöst: als gelöst(1) setzen und dp_score erhöhen
            elif request.form['dp_vergleich'] == 'guenstigste':
                if session['dp_vergleich'] is None:
                    session['dp_vergleich'] = 1
                    session['dp_score'] = session['dp_score'] + 5
            

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
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt1.html')

@app.route('/decepdive_produkt2')
def decepdive_produkt2():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt2.html')

@app.route('/decepdive_produkt3')
def decepdive_produkt3():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt3.html')

@app.route('/decepdive_produkt4')
def decepdive_produkt4():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt4.html')

@app.route('/decepdive_produkt5')
def decepdive_produkt5():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt5.html')

@app.route('/decepdive_produkt6')
def decepdive_produkt6():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt6.html')

@app.route('/decepdive_produkt7')
def decepdive_produkt7():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt7.html')

@app.route('/decepdive_produkt8')
def decepdive_produkt8():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_produkt8.html')


@app.route('/decepdive/warenkorb')
def decepdive_warenkorb():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb.html')

@app.route('/decepdive/warenkorb/konto')
def decepdive_warenkorb2():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb2.html')

@app.route('/decepdive/warenkorb/Daten')
def decepdive_warenkorb3():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb3.html')

@app.route('/decepdive/warenkorb/Übersicht')
def decepdive_warenkorb4():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb4.html')


@app.route('/decepdive/warenkorb/zahlen')
def decepdive_warenkorb5():
    initialize_session()
    if session['level_fortschritt'] >= 2:
        return redirect(url_for('home_intro'))
    return render_template('decepdive/decepdive_warenkorb5.html')

@app.route('/decepdive/ende_lv2')
def ende_lv2():
    initialize_session()
    if session['level_fortschritt'] < 2:
        # Wenn der Countdown abgelaufen und an dem Punkt nichts im Warenkorb ist,wird als Strafe der 
        # 'Geld Score' runtergesetzt
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
        
    # Liste mit den Lösungen der Spieler*in für alle Dark Patterns in level 2
    dp_list_lv2 = [ session['dp_cookielv2_trickquestion'], 
                    session['dp_cookielv2_trickquestion2'],
                    session['dp_cookielv2_berechtigt'], 
                    session['dp_vergleich'], 
                    session['dp_preticked_monatl'],
                    session['dp_sneakinbasket'],
                    session['dp_hiddennewsletter'],
                    session['dp_misdirect_login'], 
                    session['dp_misdirect_konto_erstellen'], 
                    session['dp_misdirect_spende'] ]
    
    # speicher die Lösungen aller Dark Patterns für diese Session in CSV für Evaluierung
    write_dp_ergebnisse_csv()

    # Setze levle_fortschritt auf null und leite damit den Abschluss des Spiels ein
    session['level_fortschritt'] = 2

    return render_template('decepdive/ende_lv2.html', dp_list_lv2 = dp_list_lv2)

########################### Datenspeicherung ##################################  
def write_dp_ergebnisse_csv():
    with open('ergebnisse/dark_pattern_results.csv', mode='a') as csv_file:
        fieldnames = [  'session_id', 
                'dp_open_cookiemanager_lv1',
                'dp_cookie_lv1', 
                'dp_berechtiges_interesse_lv1',
                'dp_cookiemisdirection_lv1',
                'dp_nagging_level1', 
                'dp_roachmotel1', 
                'dp_misdirect_kuendigen', 
                'dp_trickquestion1',
                'dp_shaming_lv1',
                'dp_roachmotel2', 
                'dp_cookielv2_trickquestion',
                'dp_cookielv2_trickquestion2',
                'dp_cookielv2_berechtigt', 
                'dp_vergleich', 
                'dp_preticked_monatl', 
                'dp_sneakinbasket',
                'dp_hiddennewsletter', 
                'dp_misdirect_login', 
                'dp_misdirect_konto_erstellen', 
                'dp_misdirect_spende' ] 
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        file_exists = os.path.isfile('ergebnisse/dark_pattern_results.csv')
        if not file_exists:
            writer.writeheader()
        writer.writerow({item: session[item] for item in fieldnames})

""" Funktion um CSV zu schreiben
    inputs: 
        data_list(liste mit listen): jedes Listenelement besteht aus einem Key(item-ID) und dem dazugehörigen Wert
        dateiname: name der CSV-Datei in der geschrieben werden soll """
def write_fragebogen_csv(data_list, dateiname):
        with open('ergebnisse/'+dateiname , mode='a') as csv_file:
            #initielisiere Fieldlist
            fieldnames= []
            for itemID, itemValue in data_list:
                fieldnames.append(itemID)
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 

            file_exists = os.path.isfile('ergebnisse/fragebogen_SUS.csv')
            if not file_exists:
                writer.writeheader()  
            writer.writerow({itemID: itemValue for itemID, itemValue in data_list})

################################## Fragebögen ##################################
@app.route('/fragebogen-bedienbarkeit')
def fragebogen():
    return render_template('home/fragebogen.html', status='')

@app.route('/fragebogen-allgemein', methods=['POST'])
def fragebogen_SUS():
    if request.method == 'POST':
        item_list= ['gerne_oft', 'komplex', 'einfach', 'hilfe',
                    'funktionen_integriert', 'inkonsistenzen', 
                    'umgang_lernen', 'umstaendlich',
                    'benutzung_sicher', 'musste_lernen' ]
        # liste, in der die Daten gespeichert werden, die unique session ID hinzufügen
        data_list = [ ['session_id', session['session_id']] ]
        for itemID in item_list:
            if itemID in request.form:
                 data_list.append([itemID, request.form[itemID]])
            else:
                status= ' Bitte alle Fragen beantworten'
                return render_template('home/fragebogen.html', status=status )

        write_fragebogen_csv(data_list, 'fragebogen_SUS.csv')

    return render_template('home/fragebogen2.html', )

@app.route('/vp-stunden', methods=['POST'])
def fragebogen_allgemein():
    if request.method == 'POST':
        # liste, in der die Daten gespeichert werden. Die unique session ID an index 0 hinzufügen
        data_list = [ ['session_id', session['session_id']] ]
        # für jedes item key und request.form daten als liste in data_list speichern
        for itemID in  ['interesse_gefoerdert', 'viel_gelernt', 'aufmerksamkeit', 'spass']:
            if itemID in request.form:
                 data_list.append([itemID, request.form[itemID]])
            else:
                status= ' Bitte alle Fragen beantworten'
                return render_template('home/fragebogen2.html', status=status )
        
        # daten in CSV schreiben und speichern
        write_fragebogen_csv(data_list, 'fragebogen_allgemein.csv')
    return render_template('home/fragebogen3.html', validation='', show_feedback_form= False)

@app.route('/fragebogen-abgeschlossen', methods=['POST'])
def fragebogen_vp():
    # liste, in der die Daten gespeichert werden
    data_list = []
    # für jedes item key und request.form daten als liste in data_list speichern
    for itemID in  ['name', 'matrikelnr']:
        if itemID in request.form:
                data_list.append([itemID, request.form[itemID]])
        else:
            return render_template('home/fragebogen2.html', validation='Bitte alle Felder angeben!' )
        
    write_fragebogen_csv(data_list, 'VP_Stunden.csv')
    show_feedback_form = True

    return render_template('home/fragebogen3.html', 
                           validation='Erfolgreich abgeschickt. Vielen Dank',
                           name =  request.form['name'],
                           matrikelnr = request.form['matrikelnr'],
                           show_feedback_form = show_feedback_form)

@app.route('/fragebogen-abgeschlossen/feedback', methods=['POST'])
def feedback_form():
    if 'feedback' in request.form:
        csv_list = [['feedback', request.form['feedback']]]
        write_fragebogen_csv(csv_list, 'Feedback.csv')

    return redirect(url_for('home_intro'))




