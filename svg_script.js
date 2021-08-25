
/*
document.getElementById('circle2').addEventListener('click', function(e) {
    e.currentTarget.setAttribute('fill', '#ff00cc');
})
*/


function setState() {
    var map = document.getElementById('map').contentDocument;
    var updatedStyle = "fill:green;stroke:#ffffff;stroke-opacity:1;fill-opacity:1;stroke-width:0.25;stroke-miterlimit:4;stroke-dasharray:none";
    var states = map.getElementsByTagName('path');
    //console.log(states[0]);

    
    for (i=0; i<states.length - 1; i++) {
        // Loops through each state; does not loop through last <path>, which is for state borders
        //states[i].setAttribute('style', 'fill:#d3d3d3;stroke:#ffffff;stroke-opacity:1;fill-opacity:1;stroke-width:0.25;stroke-miterlimit:4;stroke-dasharray:none')
        states[i].addEventListener('click', function(e) {
            e.currentTarget.setAttribute('style', updatedStyle);
        })
        //states[i].setAttribute('style', updatedStyle);
    } 
      
}

/*
function setState() {
    var map = document.getElementById('map').contentDocument;
    var tx = map.getElementById('TX');
    var la = map.getElementById('LA');
    var updatedStyle = "fill:darkblue;stroke:##ffffff;stroke-opacity:1;fill-opacity:1;stroke-width:0.75;stroke-miterlimit:4;stroke-dasharray:none";

    tx.setAttribute('class', 'country');
    la.setAttribute('class', 'country');

    for (i=0; i<2; i++) {
        console.log(map.getElementsByClassName('country')[i]);
        map.getElementsByClassName('country')[i].setAttribute('style', updatedStyle);
    }
}
*/


window.addEventListener('load', setState);
