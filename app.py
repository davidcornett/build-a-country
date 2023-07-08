from array import array
from ast import Str
from flask import Flask, render_template, request, flash, jsonify
from flask_cors import CORS
import os
from county import County
from country import Country
import csv

#from svg.path import parse_path
#from svg.path.path import Line
from xml.dom import minidom


county_adjacencies = [] # array of linked lists

# global var: TBD replace with DB calls
player_country = None

# globals to control country sizes - TBD replace when different modes allowed
max_area = 10000
min_area = 0

# Configuration
app = Flask(__name__)
CORS(app)  # enable CORS for all routes

def main():
    adjacency()
    
    """
    for e in county_adjacencies:
        print(e)
    """
    #print(int(county_adjacencies[0][0]) + 5)

# Routes 
@app.route('/')
def root():
    return "not implemented"


@app.route('/svg')
def svg():
    path_dict = {}
    doc = minidom.parse('static/usa-all-counties.svg')
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    paths = [path for path in doc.getElementsByTagName('path')]
    
    for p in paths:
        for county in player_country.get_counties():
            if p.getAttribute('id') == county.get_id():
                #print(p.getAttribute('id'))
                path_dict[p.getAttribute('id')] = {"d":p.getAttribute('d')}

    doc.unlink()

    """
    paths["id"] = "01069"
    paths["d"] = "M 409.67498,255.323 L 413.28898,254.994 L 413.17198,255.336 L 413.09598,255.67 L 413.24898,256.585 L 413.36098,256.846 L 413.45598,256.9 L 413.55098,256.9 L 413.63298,256.923 L 414.15398,257.496 L 414.23598,257.643 L 414.35498,257.9 L 414.67798,258.834 L 409.35098,259.482 L 409.26498,258.46 L 409.08798,256.882 L 408.00198,257.067 L 406.63198,257.211 L 407.02098,256.233 L 407.08298,256.179 L 407.33998,256.094 L 407.52498,256.085 L 407.69998,256.094 L 408.07398,256.183 L 408.35898,256.26 L 408.85498,256.306 L 409.02198,256.291 L 409.71998,255.692 L 409.67498,255.323"
    paths["inkscape:label"] = "Houston, AL"
    """

    return jsonify(path_dict)

    return "44"

@app.route('/map', methods=['GET', 'POST'])
def map():
    
    if request.method == 'POST':
        
        countyID_string = request.form['counties']
        countyID_list = process_countyID(countyID_string)
        global player_country
        player_country = createCountry(countyID_list)
 
        # check that country is contigious and within allowed area range
        if not check_validity(player_country):
            return "Error: invalid country"
        
        #(player_country.get_pop())
        player_country.set_races()
        #player_country.get_races()

        # create_new_map([x.get_id() for x in player_country.get_counties()], "namey")
 
        return render_template("country.html", country = player_country)

    else:
        return render_template("map.html", max_area = max_area)

@app.route('/get_ids')
def get_ids() -> array:
    return jsonify([x.get_id() for x in player_country.get_counties()])

@app.route('/get_area/<id>')
def get_area(id) -> str:
    c = County(str(id))
    return jsonify(c.get_area())


def create_new_map(county_ids: list, name: str) -> None:
    new_file = open("static/template.svg")
    content = new_file.read()
    print(content[0:40])
    """
    for x in county_ids:
        print("new map: %s", x)
    """
    old_file = open("static/usa-all-counties.svg.svg")
    #new_file.write("ffff") 
    new_file.close()
    old_file.close()



def process_countyID(id: str) -> list:
    output = []
    elem = ''

    # remove leading-0s due to county id coding in SVG
    def remove_leading_zero(id: str):
        return id[1:] if id.startswith('0') else id
    
    for char in id:
        # character groups terminating with comma should be appended to list
        if char == ',':
            output.append(remove_leading_zero(elem))
            elem = ''
        else:
            elem += char
    
    output.append(remove_leading_zero(elem))  # add last character group, not terminating with comma
    return output

def createCountry(county_ids: list) -> object:
    # returns Country, comprised of Counties
    county_list = [County(id) for id in county_ids] # create list of County objects from list of county IDs
    return Country(county_list)


def adjacency():
    county_counter = 0;
    with open('county_neighbors.csv') as file:
        data = list(csv.reader(file, delimiter=','))
        county_adjacencies.append(data[1])
        length = len(data)
        for i in range(2, length):
            if county_adjacencies[-1][0] == data[i][0]:
                county_adjacencies[-1].append(data[i][1])
            else:
                county_adjacencies.append(data[i])


def check_validity(country: object) -> bool:
    # CHECK 1: AREA
    if country.get_area() not in range(min_area, max_area):
        return False

    # CHECK 2: ADJACENCY
    county_ids = [county.get_id() for county in country.get_counties()]

    starting_node = country.get_counties()[0].get_id()  # get a county ID from country
    
    # BFS traversal of graph - if not all counties selected are visited, country is invalid
    visited = [starting_node]
    queue = [starting_node]
    counter = 0

    while queue:
        current_node = queue.pop(0)
        counter += 1

        # get adjacent nodes of current node
        adjacent_nodes = adj_binary_search(int(current_node))

        for node in adjacent_nodes:
            if node not in visited and node in county_ids:
                visited.append(node)
                queue.append(node)

    return True if counter == len(county_ids) else False


def adj_binary_search(id: int) -> bool:
    
    # get lowest and highest county id from global array of arrays 
    low = 0
    high = len(county_adjacencies)
    
    while True:

        mid = (low + high)//2
        mid_item = int(county_adjacencies[mid][0])
        
        if id == mid_item:
            #print("returning adjacencies: " + str(county_adjacencies[mid][1:]))
            return county_adjacencies[mid][1:]

        elif (low == high):
            break       
        elif id > mid_item:
            low = mid + 1
        else:
            high = mid - 1

        #print("low = " + str(low) + " high = " + str(high))
    return False



# Listener
if __name__ == "__main__":
    # bind to PORT if defined, otherwise use default
    main()
    port = int(os.environ.get('PORT', 6205))
    app.run(port=port) 
