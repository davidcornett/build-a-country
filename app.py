from array import array
from flask import Flask, render_template, request, flash, jsonify
import os
from county import County
from country import Country

# global var: TBD replace with DB calls
player_country = None


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
        global player_country
        player_country = createCountry(countyID_list)
        
        print(player_country.get_pop())

        # create_new_map([x.get_id() for x in player_country.get_counties()], "namey")
 
        return render_template("country.html", country = player_country)

    else:
        return render_template("map.html")

@app.route('/get_ids')
def get_ids() -> array:
    return jsonify([x.get_id() for x in player_country.get_counties()])
    #return jsonify({'A':12345, 'B':764})
    #return jsonify([1, 2, 3, 4])



def create_new_map(county_ids: list, name: str) -> None:
    new_file = open("static/empty_map.svg")
    content = new_file.read()
    print(content[0:40])
    """
    for x in county_ids:
        print("new map: %s", x)
    """
    old_file = open("static/test2.svg")
    #new_file.write("ffff") 
    new_file.close()
    old_file.close()



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
    # returns Country, comprised of Counties
    county_list = [County(id) for id in county_ids] # create list of County objects from list of county IDs
    return Country(county_list)

# Listener
if __name__ == "__main__":
    # bind to PORT if defined, otherwise use default
    port = int(os.environ.get('PORT', 6205))
    app.run(port=port) 
