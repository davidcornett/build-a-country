from flask import Flask, render_template, request, flash
import os
from county import County
from country import Country

# Configuration
app = Flask(__name__)

# Routes 
@app.route('/')
def root():
    return '4'

@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':

        countyID_string = request.form['counties']
        countyID_list = process_countyID(countyID_string)
        player_country = createCountry(countyID_list)

        for i in player_country.get_counties():
            print(i.get_name())
        
        return "test"

    else:
        return render_template("map.html")

def process_countyID(id: str) -> list:
    output = []
    elem = ''
    for char in id:
        # character groups terminating with comma should be appended to list
        if char == ',':
            output.append(elem)
            elem = ''
        else:
            elem += char
    output.append(elem)  # add last character group, not terminating with comma
    return output

def createCountry(county_ids: list) -> object:
    county_list = []
    for id in county_ids:
        county_list.append(County(id))

    return Country(county_list)

# Listener
if __name__ == "__main__":
    # bind to PORT if defined, otherwise use default
    port = int(os.environ.get('PORT', 6205))
    app.run(port=port) 
