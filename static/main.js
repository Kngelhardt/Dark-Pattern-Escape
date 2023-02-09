

/* Funktion um Elemente verschwinden oder erscheinen zu lasssen */
function show__hide_div(a){
    if(document.getElementById(a).style.display != "none"){
        document.getElementById(a).style.display = "none";
    }else{
        document.getElementById(a).style.display = "inline";
    }
}