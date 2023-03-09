
/* Funktion um Elemente verschwinden oder erscheinen zu lasssen */
function show_hide_div(a){
    console.log(document.getElementById(a), a);
    if(document.getElementById(a).style.display != "none"){
        document.getElementById(a).style.display = "none";
    }else{
        document.getElementById(a).style.display = "inline";
    }
}

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
        if (isJson(post_object)){
            req.send(JSON.stringify(post_object));
        }else{
            req.send(JSON.stringify({ object: post_object}));
        }
        
    }
}

/*  sended POST request and die Flask funktion 'change_session', 
    dort werde Flask session-Werte mit den im json_obj enthaltenen key-value-Paaren geupdated
    input:
        json_obj: sollte zwei Werte enthalten:
            session_key: Key der session die aufgerufen werden soll
            session_value: neuer wert für den session key */
function set_session_value(json_obj){
    ajax_request('POST', '/change-session', json_obj);
}

/*  Funktion um die Werte der Progressbars upzudaten und anschließend in der Session zu speihern
    Session-Keys:
    dp_score: Permanent steigend
    geld_score: update nach levelende
    data_score (unterteilt in zwei variable mit 50 % für die jeweiligen level): permanent sinkend. Kann im richtigen menü wieder zurückgesetzt werden
    inputs:
    bar: die id der Progress-Bar, die geändert werden soll
    value_now: Aktueller Wert der Bar
    value_add: Wert, um den sich die Bar-ändern soll*/
function progress_add(bar, value_now, value_add){
    var  value_after = value_now +   value_add;
    console.log(bar, value_now, value_add, value_after)

    if(document.getElementById(bar) == document.getElementById("dp_score_bar")){
        document.getElementById(bar).style.width = value_after + '%';
    }
    else if(document.getElementById(bar) == document.getElementById("geld_bar")){
        document.getElementById(bar).style.width = value_after + '%';
    }
    else if(document.getElementById(bar) == document.getElementById("data_bar")){
        document.getElementById(bar).style.width = value_after + '%';
    }
}

/* Countdown Timer. Nach ablauf wird weitergeleitet zur spielübersicht */
function level_countdown(zeit_state, level_fortschritt){
    // zeit_state ist der aktuelle stand der sekundens
    counter = zeit_state;
    // jede sekunde/1000ms wird counter herunter gesetzt
    countdown = setInterval( function(){
        // Wenn counter bei null sekunden 
        if (counter < 0){
            // Setze level_fortschritt auf 1 oder 2, damit das richtige zwischenmenü angezeigt wird
            if(level_fortschritt == 0){
                window.location.href = '/ende_lv1';
            }else if(level_fortschritt == 1){
                ajax_request('GET', "/decepdive/ende_lv2", null);
            }
        } else {
            // Sekunden runterzählen
            counter = counter -1;
            // die Zeitanzeige inkl. Text in der Fußleiste anktualisieren
            document.getElementById('zeit_bar').style.width = counter/3 +'%';
            document.getElementById('zeit_anzeige').innerText = counter + "s";
            // update countdown value in session
            ajax_request(
                'POST', //method
                '/update_timer', //url für timer update, returns: '', 204
                Math.floor(  
                        // funktion um länge der bar in % abzurufen 
                        // multipliziert mit 3 um auf die max. 300 sekunden zu skalieren: 
                        // ((child.width / parent.width) *100 ) *3
                        (document.getElementById('zeit_bar').clientWidth / document.getElementById('container_zeit_bar').clientWidth) * 300
                    ) 
            );
        }
    }, 9999999999); 
}

/* Timer der dei Uhrzeit darstellt. 
Zählt in 100ms-Schritten von null hoch und wenn 24 erricht ist, fängt er wieder bei 0 an */
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

function ist_erreichbar(){
    console.log('test')
    // Button funktioniert nur, wenn der starte_uht timer zwischen 14 und 16 ist
    if(parseInt(document.getElementById('uhr').textContent) >= 14 && parseInt(document.getElementById('uhr').textContent) <= 16){
        console.log('test2')
        // Backend update:
        set_session_value({'dp_score': 4, 'dp_roachmotel2': true});
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


    





