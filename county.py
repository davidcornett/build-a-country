import psycopg2

# Configuration
con = psycopg2.connect(dbname='map_game', user='postgres', host='localhost', password='applePython@7788')
cur = con.cursor()

class County:
    def __init__(self, id: str):
        self._id = id
        self._pop = self.set_pop()
        self._name = self.set_name()
        con.commit()

    def get_id(self) -> str:
        return self._id

    def get_pop(self) -> int:
        return self._pop

    def get_name(self) -> str:
        return self._name

    def set_name(self) -> str:
        name_query = """ SELECT countyName FROM counties WHERE countyID =%s;"""
        cur.execute(name_query, [self._id])
        return cur.fetchone()[0]

    def set_pop(self) -> int:
        pop2020_query =   """
                    SELECT pop2020 FROM counties_pop_estimates 
                    JOIN counties on counties_pop_estimates.countyID = counties.countyID
                    AND counties.countyID =%s;
                    """
        
        cur.execute(pop2020_query, [self._id])
        return cur.fetchone()[0]
    
    