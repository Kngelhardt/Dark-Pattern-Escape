

/* Funktion um Elemente verschwinden oder erscheinen zu lasssen */
function show__hide_div(a){
    if(document.getElementById(a).style.display != "none"){
        document.getElementById(a).style.display = "none";
    }else{
        document.getElementById(a).style.display = "inline";
    }
}

/*  dp_score: Permanent steigend
    geld_score: update nach levelende
    data_score (unterteilt in zwei variable mit 50 % für die jeweiligen level): permanent sinkend. Kann im richtigen menü wieder zurückgesetzt werden  
    bar: die Progress-Bar, die geändert werden soll
    val: Wert, um den sich die Bar-ändern soll (relevant nur für geld?)*/
function progress_add(bar, value){
    if(document.getElementById(bar) == document.getElementById("dp_score_bar")){
        var  dp_score = value + 2;
        document.getElementById(bar).style.width = dp_score + '%';
        
    }
    if(document.getElementById(bar) == document.getElementById("geld_bar")){
        var  geld_score = value + 2;
        document.getElementById(bar).style.width = geld_score + '%';
    }
    if(document.getElementById(bar) == document.getElementById("data_bar")){
        var  data_score = value - 2;
        document.getElementById(bar).style.width = data_score + '%';
    }
}

function starte_uhr(){
    var uhrzeit = setInterval(uhr_timer, 200);
}

function uhr_timer() {

    var uhr = document.getElementById('uhr');
    var d = new Date();
    var m = Math.round(d.getMilliseconds() /10);
    var s = d.getSeconds();
    if (s >= 24){
        clearInterval(uhrzeit);
        var uhrzeit = setInterval(uhr_timer, 200);
    }
    uhr.textContent = s+ ":" + m  
}

function reset_timer(timer, intervall, funktion){
    timer = setInterval(funktion, intervall);
}


