import psycopg2
from psycopg2 import sql

# Configuration
con = psycopg2.connect(dbname='map_game', user='davidcornett', host='localhost', password='applePython@7788')
cur = con.cursor()

class County:
    def __init__(self, id: str):
        self._id = id
        self._pop = self.set_pop()
        self._name = self.set_name()
        self._racial_breakdown = None
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
        pop_query = """
                SELECT total_pop FROM countyid_year
                WHERE year=2021 AND fips=%s;
                """
        
        cur.execute(pop_query, [self._id])
        return cur.fetchone()[0]

    def set_races(self) -> None:
        races = ['black', 'native', 'asian', 'pac_isl', 'two_plus_races', 'hispanic', 'white_not_hispanic']
        
        query_syntax = """
                SELECT {} FROM countyid_year
                WHERE year=2021 AND fips=%s;
                """
        
        query = sql.SQL(query_syntax).format(sql.SQL(", ").join(map(sql.Identifier, races)))
        cur.execute(query, [self._id])
        query_result = cur.fetchall()[0]
        d = {}
        for i in range(len(races)):
            d[races[i]] = query_result[i]

        
        self._racial_breakdown = d
    
    
    def get_area(self) -> float:
        area_query = """ SELECT size from counties WHERE countyID =%s;"""
        cur.execute(area_query, [self._id])
        return cur.fetchone()[0]
    
    
