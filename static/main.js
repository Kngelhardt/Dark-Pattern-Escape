

/* Funktion um Elemente verschwinden oder erscheinen zu lasssen */
function show__hide_div(a){
    if(document.getElementById(a).style.display != "none"){
        document.getElementById(a).style.display = "none";
    }else{
        document.getElementById(a).style.display = "block";
    }
}

/*  dp_score: Permanent steigend
    geld_score: update nach levelende
    data_score (unterteilt in zwei variable mit 50 % für die jeweiligen level): permanent sinkend. Kann im richtigen menü wieder zurückgesetzt werden  
    bar: die Progress-Bar, die geändert werden soll
    val: Wert, um den sich die Bar-ändern soll (relevant nur für geld?)*/
function progress_add(bar, val){
    if(document.getElementById(bar) == document.getElementById("dp_score_bar")){
        document.getElementById(bar).style.width = "{{ dp_score }}%";
    }
    if(document.getElementById(bar) == document.getElementById("geld_bar")){
        document.getElementById(bar).style.width = "{{ geld_score }}%";
    }
    if(document.getElementById(bar) == document.getElementById("data_bar")){
        document.getElementById(bar).style.width = "{{ data_score }}%";
    }
}