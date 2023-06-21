import csv
from collections import defaultdict

county_adjacencies = [] # array of linked lists

class Country:
    def __init__(self, counties: list):
        self._counties = counties
        self._area = sum(county.get_area() for county in self._counties)
        self._pop = sum(county.get_pop() for county in self._counties)
        self._racial_breakdown = None
    
    def get_counties(self):
        return self._counties

    def get_pop(self) -> int:
        return self._pop
    
    def get_area(self) -> float:
        return self._area

    def check_validity(self):
        pass


    def set_races(self):
        races = ['black', 'native', 'asian', 'pac_isl', 'two_plus_races', 'hispanic', 'white_not_hispanic']
        racial_breakdown = defaultdict(int)
        for i in range(len(self._counties)):
            self._counties[i].set_races()
            for j in range(len(races)):
                racial_breakdown[races[j]] += self._counties[i]._racial_breakdown[races[j]]

        self._racial_breakdown = racial_breakdown
    
    def get_racial_percentage(self, race: str) -> float:
        return self._racial_breakdown[race]/self._pop


