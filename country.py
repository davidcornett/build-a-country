


class Country:
    def __init__(self, counties: list):
        self._counties = counties
    
    def get_counties(self):
        return self._counties

    def get_pop(self) -> int:
        return sum(county.get_pop() for county in self._counties)

