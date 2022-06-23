//var selectedCounties = [];

/*
function getCountyIDs() {
    fetch('http://127.0.0.1:6205/get_ids')
    .then(response => response.json())
    .then(json => {
        //console.log(json[1]);
        //selectedCounties = JSON.stringify(json);
        //selectedCounties = JSON.parse(json);
        json.forEach((e) => {
            //console.log(e)
            selectedCounties.push(e);
        });
    })

    //selectedCounties = [2, 3, 4, 5];

}
/*
function getCountyIDs() {
    let url = 'http://127.0.0.1:6205/get_ids';
    selectedCounties.push(fetch(url)
    .then(response => response.json())
    );
}

*/

async function getCountyIDs(){
    
    let url = 'http://127.0.0.1:6205/get_ids';
    let test = [];
    await fetch(url).then(
        async (value) => {
            return await value.json()
        }
    ).then(
        (value) => {
            test = value
        }
    )
    return test;
    //console.log(selectedCounties);
    


}

async function setCounties() {
    //var selectedCounties = [1, 2];
    var selectedCounties = await getCountyIDs();

    console.log(selectedCounties);
    selectedCounties.forEach((elem) => {
        console.log(elem)
    });
    
    var map = document.getElementById('map').contentDocument;
    var updatedStyle = "fill:green;stroke:#ffffff;stroke-opacity:1;fill-opacity:1;stroke-width:0.25;stroke-miterlimit:4;stroke-dasharray:none";
    var defaultStyle = "font-size:12px;fill:#d0d0d0;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel";
    var invisible = "visibility:hidden";
    var states = map.getElementsByTagName('path');
    var currentCounty = null;

    for (i=0; i<states.length - 1; i++) {
        // Loops through each county; does not loop through last <path>, which is for state borders

        // DESELECT county 
        
        // SELECT county

        //d3.select("#ID");

        let id = states[i].getAttribute('id')

        if (selectedCounties.includes(id)) {
            states[i].setAttribute('style', updatedStyle);

        } else {
            states[i].setAttribute('style', invisible);
        } 
    }              
}

window.addEventListener('load', setCounties);
