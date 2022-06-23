
//to-do: click to deselect county

var selectedCounties = [];

function incrCountyNum() {
    //increase counter in html by 1
    document.getElementById('countyCount').innerText ++;
}

function decrCountyNum() {
    //decrease counter in html by 1
    document.getElementById('countyCount').innerText --;
}

function setCounties() {
    //console.log(document.getElementById('map').contentDocument);
    var map = document.getElementById('map').contentDocument;
    var updatedStyle = "fill:green;stroke:#ffffff;stroke-opacity:1;fill-opacity:1;stroke-width:0.25;stroke-miterlimit:4;stroke-dasharray:none";
    var defaultStyle = "font-size:12px;fill:#d0d0d0;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel";
    var states = map.getElementsByTagName('path');
    var currentCounty = null;

    for (i=0; i<states.length - 1; i++) {
        // Loops through each county; does not loop through last <path>, which is for state borders

        // DESELECT county 
        
        // SELECT county


        // select or deselect a county upon click, depending on whether it was already selected
        states[i].addEventListener('click', function(e) {
            let id = e.currentTarget.getAttribute('id')

            // if already selected - clear formatting, remove from array, and decrement counter
            if (selectedCounties.includes(id)) {
                e.currentTarget.setAttribute('style', defaultStyle);
                selectedCounties = selectedCounties.filter(function(f) {return f !== id })
                decrCountyNum()

            // if not selected yet - apply special formatting, add to array, and increment counter
            } else {
                e.currentTarget.setAttribute('style', updatedStyle);
                selectedCounties.push(id); 
                incrCountyNum();
            } 
        })        

        // when user hovers over a county, 'Current County' display shows the county name
        states[i].addEventListener('mouseover', function(f) {
            currentCounty = f.currentTarget.getAttribute('inkscape:label');
            let countyHolder = document.getElementById('currentCounty');
            countyHolder.innerText = currentCounty;
        })
    }      
}

function getCounties() {
    let counties = document.getElementById('counties');
    counties.value = selectedCounties;
}

window.addEventListener('load', setCounties);
document.querySelector('#submit_country').addEventListener('click', getCounties);
document.getElementById('countyCount')
