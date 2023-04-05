/* -------------------------------------------FLASK REQUEST FUNKTIONEN--------------------------------------------------------------------- */

/* Testen ob post_object im JSON Format ist */
function isJson(str) {
    var objectConstructor = ({}).constructor;
    if (str.constructor === objectConstructor) {
        return true;
    } else{
        return false;
    }
}

/* ajax test (no status tests) */
function ajax_request(method, url, post_object){
    const req= new XMLHttpRequest();
    if(method == 'GET'){
        // konfiguration des Requests
        req.open(method, url);
        // senden des Requests
        req.send();
        return 
    }else if(method =='POST'){
        req.open(method, url, true);
        req.setRequestHeader('Content-Type', 'application/json')
        // Wenn 'post_object' ist JSON type
        if (isJson(post_object)){
            req.send(JSON.stringify(post_object));
        // Sonst 'post_object' zu JSON schreiben
        }else{
            req.send(JSON.stringify({ object: post_object}));
        }
    }
}

/*  sended POST request and die Flask funktion 'change_session', 
    dort werde Flask session-Werte mit den im json_obj enthaltenen key-value-Paaren geupdated
    input:  json_obj: sollte zwei Werte enthalten:
                session_key: Key der session die aufgerufen werden soll
                session_value: neuer wert für den session key */
function set_session_value(json_obj){
    ajax_request('POST', '/change-session', json_obj);
}

/* Erhöhe oder verringere Scores nur, wenn DP noch nit schon einmal gelöst */
function set_wenn_nicht_geloest(dark_pattern_value, json_obj){
    /* Check, ob das Pattern schon gelöst wurde, wenn nein -> update session */
    if (dark_pattern_value == 'None'){
        set_session_value(json_obj);
    }
}

/* Delay beim aufrufen einer neuen Seite, damit ein POST request um die session zu updaten noch durchgeht */
function url_delay_set_session(dark_pattern_value, url, json_obj){
    set_wenn_nicht_geloest(dark_pattern_value, json_obj);

    delay = setInterval(function(){
        window.location.href = url;
        clearInterval(delay)
    },70);
}

/* -------------------------------------------Level Übergreifende Funktionen--------------------------------------------------------------------- */
/*  Funktion um die Werte der Progressbars zu aktualisieren.
    inputs:
        bar: die id der Progress-Bar, die geändert werden soll
        value_now: Aktueller Wert der Bar
        value_add: Wert, um den sich die Bar-ändern soll*/
function progress_add(bar, value_now_id, value_add){
    var value_now = parseInt(document.getElementById(value_now_id).textContent)
    var  value_after = value_now + value_add;

    if(document.getElementById(bar) == document.getElementById("dp_score_bar")){
        document.getElementById(bar).style.width = value_after + '%';
        document.getElementById('dp_score_text').innerText = value_after;
    }
    else if(document.getElementById(bar) == document.getElementById("geld_bar")){
        document.getElementById(bar).style.width = value_after + '%';
        document.getElementById('geld_text').innerText = value_after;
    }
    else if(document.getElementById(bar) == document.getElementById("data_bar")){
        document.getElementById(bar).style.width = value_after + '%';
        document.getElementById('data_text').innerText = value_after;
    }
}

/* Funktion um Elemente verschwinden oder erscheinen zu lasssen */
function show_hide_div(a){
    if(document.getElementById(a).style.display != "none"){
        document.getElementById(a).style.display = "none";
    }else{
        document.getElementById(a).style.display = "inline";
    }a
}

/* Forms: Validität wieder zu valid setzen */
function clearValidity(input_name){
    document.getElementById(input_name).setCustomValidity('');
}

/* -----------------------------------------------TIMER FUNKTIONEN--------------------------------------------------------------------- */
/* Countdown Timer. Nach ablauf wird weitergeleitet zur spielübersicht */
function level_countdown(zeit_state, level_fortschritt){
    // zeit_state ist der aktuelle stand der sekundens
    counter = zeit_state;
    // jede sekunde/1000ms wird counter herunter gesetzt
    countdown = setInterval( function(){
    // Wenn counter bei null sekunden 
        if (counter <= 0){
            // Setze level_fortschritt auf 1 oder 2, damit das richtige zwischenmenü angezeigt wird
            if(level_fortschritt == 0){
                window.location.href = '/ende_lv1';
            }else if(level_fortschritt == 1){
                window.location.href = '/decepdive/ende_lv2'
            }
        } else {
            // Sekunden runterzählen
            counter = counter -1;
            // die Zeitanzeige inkl. Text in der Fußleiste anktualisieren
            document.getElementById('zeit_bar').style.width = counter/3 +'%';
            document.getElementById('zeit_anzeige').innerText = counter + "s";
            // session['countdown'] wird alle 3 sekunden aktualisiert
            if(counter%3 == 0){
            // update countdown value in session
                ajax_request(
                    'POST', //method
                    '/update_timer', //url für timer update, returns: '', 204
                    counter
                    );
            }
        }
    },10000000); 
}


/* Timer der eine Digitale Uhr Uhrzeit anzeigen lässt. 
Zählt in 150ms-Schritten von null hoch. Wenn 24 erricht ist, fängt er wieder bei 0 an */
function starte_uhr(){
    var stunde = 0
    // jede 300ms 
    uhrzeit = setInterval(function(){
        // Überschreibe den uhr text mit aktueller Stunde
        document.getElementById('uhr').textContent = stunde;
        // erhöhe stundenzahlt um 1 
        stunde = stunde + 1
        // Reset nach 24 Stunden
        if(stunde >= 24){
            stunde = 0
        }
    }, 150); 
}

/* Ruft URL '/ende_lv1' auf, wenn die var 'stunde' in starte_uhr() zwischen 14 und 16 ist*/
function ist_erreichbar(){
    // Button funktioniert nur, wenn der starte_uht timer zwischen 14 und 16 ist
    if(parseInt(document.getElementById('uhr').textContent) >= 14 && parseInt(document.getElementById('uhr').textContent) <= 16){
        // Backend update: 
        set_session_value({'dp_score': 5, 'dp_roachmotel2': 1});
        // Frontend update
        progress_add('dp_score_bar','dp_score_text', 5);
        // Halte Uhr an
        clearInterval(uhrzeit);
        // "Anrufen" Knopf verschwinden lassen
        show_hide_div('beenden_knopf');
        // Zeige den Enddialog
        show_hide_div('enddialog');
        // Gib spieler*innen 4 Sekunden Zeit zum Lesen und leite dann weiter
        var counter = 0;
        ende_delay = setInterval(function(){
            counter = counter +1;
            window.location.href = '/ende_lv1';
        }, 4000); 
    }
}
/* -------------------------------Nagging Modal öffnen in Level 1 ------------------------------------------- */
/* function load_nagging(){
    bis_oeffnung = setInterval(function(){
        modal = document.getElementById('nagging_modal')
        console.log('naggingmodal', modal)
        modal.show()
    },5000)
} */


/* -------------------------------Warenkorb-Kalkulation für level 2 ----------------------------------------- */
function calculate_total(){
    let produkpreis = parseFloat(document.getElementById('produkt_preis').textContent);
    let versandpreis = 0;
    let monatl_rabatt = 0;
    let probenpreis = 0;
    let gesamtpreis = 0;

    // Cheken ob die probe versteckt (Warenkorb schritt 1) oder nicht vorhanden ist (warenkorb schritt 4)
    // Wenn nicht probenpreis aktualisieren
    if (document.getElementById('probe_preis') != null){
        if (document.getElementById('probe_preis').style.display != "none" ){
            probenpreis = parseFloat(document.getElementById('probe_preis').textContent);
        }
    }
    // versandpreis nur in Warenkorb Schritt 4 vorhanden, daher error vermeiden
    if (document.getElementById('versand_preis')!= null) {
        versandpreis = parseFloat(document.getElementById('versand_preis').textContent);
    }
    if (document.getElementById('rabatt_monatl') != null){
        monatl_rabatt = parseFloat(document.getElementById('rabatt_monatl').textContent);
    }
    // gesamtpreis berechnen
    gesamtpreis = produkpreis + versandpreis + monatl_rabatt + probenpreis;
    // Textanzeige für Gesamtpreis aktualisieren
    document.getElementById('gesamt_preis').textContent = gesamtpreis;
    set_session_value({'warenkorb': gesamtpreis});
    
    // Value des inputfelds aktualisieren damit der preis per POST request an Flask weitergegeben werden kann
    if (document.getElementById('preis_input') != null){
        document.getElementById('preis_input').value = gesamtpreis;
    }
}

    





