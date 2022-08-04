from array import array
from flask import Flask, render_template, request, flash, jsonify
import os
from county import County
from country import Country
import csv


county_adjacencies = [] # array of linked lists

# global var: TBD replace with DB calls
player_country = None


# Configuration
app = Flask(__name__)

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
    return '4'

@app.route('/map', methods=['GET', 'POST'])
def map():
    
    if request.method == 'POST':
        
        countyID_string = request.form['counties']
        countyID_list = process_countyID(countyID_string)
        global player_country
        player_country = createCountry(countyID_list)
 
        if not check_validity(player_country):
            return "Error: invalid country"
        
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
    county_ids = [county.get_id() for county in country.get_counties()]
    #print("length of chosen ids: " + str(len(county_ids)))
    #print("length of adj: " + str(len(county_adjacencies)))

    starting_node = country.get_counties()[0].get_id()  # get a county ID from country
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
