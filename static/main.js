/* Funktion um Elemente verschwinden oder erscheinen zu lasssen */
function show_hide_div(a){
    if(document.getElementById(a).style.display != "none"){
        document.getElementById(a).style.display = "none";
    }else{
        document.getElementById(a).style.display = "inline";
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
        req.send(JSON.stringify({ object: post_object}));
    }
}

/* input:
    session_key: Key der session die aufgerufen werden soll
    session_value: neuer wert für den session key */
function set_session_value(session_key, session_value){
    const req= new XMLHttpRequest();
    // konfiguration des Requests
    req.open("POST", '/set-session', true);
    req.setRequestHeader('Content-Type', 'application/json')
    // senden des Requests mit key und value paar von input
    req.send(JSON.stringify({ [session_key]: session_value}));
}

/*  Session-Keys:
    dp_score: Permanent steigend
    geld_score: update nach levelende
    data_score (unterteilt in zwei variable mit 50 % für die jeweiligen level): permanent sinkend. Kann im richtigen menü wieder zurückgesetzt werden
    inputs:
    bar: die id der Progress-Bar, die geändert werden soll
    value_now: Aktueller Wert der Bar
    value_add: Wert, um den sich die Bar-ändern soll*/
function progress_add(bar, value_now, value_add){
    if(document.getElementById(bar) == document.getElementById("dp_score_bar")){
        var  value_after = value_now + value_add;
        document.getElementById(bar).style.width = value_after + '%';
        set_session_value('dp_score', value_after);
    }
    else if(document.getElementById(bar) == document.getElementById("geld_bar")){
        var  value_after = value_now + value_add;
        document.getElementById(bar).style.width = value_after + '%';
        set_session_value('geld_score', value_after);
    }
    else if(document.getElementById(bar) == document.getElementById("data_bar")){
        var  value_after = value_now - value_add;
        document.getElementById(bar).style.width = value_after + '%';
        set_session_value('data_score', value_after);
    }
}

/* Timer Funktionen --------------------------------------------------------------------------------------------------------------------------------------*/
function reset_timer(timer, intervall, funktion){
    timer = setInterval(funktion, intervall);
}

/* Countdown Timer. Nach ablauf wird weitergeleitet zur spielübersicht */
function level_countdown(zeit_state){
    // zeit_state ist der aktuelle stand der sekundens
    counter = zeit_state;

    // jede sekunde/1000ms wird counter herunter gesetzt
    countdown = setInterval( function(){
        // Wenn counter bei null sekunden
        if (counter < 1){
            // Setze level_fortschritt auf 1, damit das richtige zwischenmenü angezeigt wird
            ajax_request('GET', "/deceptv/ende_lv1", null);
            // Redirect zur Levelübersicht
            // 30ms puffer, damit der get request fertig ist, bevor der redirect startet
            puffer = setInterval( function(){
                window.location.href = '/home/intro';
                clearInterval(puffer);
            },35);
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
    }, 1000); 
}

function bar_laenge(){
    const a = Math.floor(
        (document.getElementById('zeit_bar').clientWidth / document.getElementById('container_zeit_bar').clientWidth) * 300
    );
    // Die width der progressbars ist in dem format 'zahl%' angegeben, letzter index des Strings mit dem '%' wird entfernt
    const b = parseInt(document.getElementById('zeit_bar').style.width.slice(0, document.getElementById('zeit_bar').style.width.length -1));
    // string zu int casten und mal 3 nehmen um die 100% auf die
    b = b*3;
    console.log(a);
    console.log(b);

    return a;
}

/* Uhr Timer */
function starte_uhr(){
    /* var date = 0.. */
    var uhrzeit = setInterval(uhr_timer, 200);
}

function uhr_timer() {

    var uhr = document.getElementById('uhr');
    var d = new Date();
    var m = Math.round(d.getMilliseconds() /10);
    var s = d.getSeconds();
    if (s >= 24){
        reset_timer(uhrzeit, 500, uhr_timer )
    }
    uhr.textContent = s+ ":" + m  
}


    





