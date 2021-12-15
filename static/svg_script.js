
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
    var states = map.getElementsByTagName('path');
    var currentCounty = null;

    for (i=0; i<states.length - 1; i++) {
        // Loops through each county; does not loop through last <path>, which is for state borders

        // when user clicks a county, style is updated and county id goes to array
        states[i].addEventListener('click', function(e) {
            e.currentTarget.setAttribute('style', updatedStyle);
            let id = e.currentTarget.getAttribute('id')
            if (selectedCounties.includes(id)) {
                alert("Already included!")
            } 
            else {
                selectedCounties.push(id); // add county id to array
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
