import os
import numpy as np
import pandas as pd
import psycopg2 as pg
from functools import cache
from geopy.geocoders import Nominatim

DATAPATH = os.path.abspath('') + "/../../data/"

class Database():
    def __init__(self):
        self.output = None
        
    def connect(self):
        return pg.connect(host="localhost", port="5432", database="bi", user="postgres", password="postgres")

    def execute(self, query, fetch=True):
            try:
                with self.connect() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query)
                        column_names = [info[0] for info in cursor.description]
                        value = (cursor.fetchall() if fetch else True)
                conn.close()
            except (Exception, pg.DatabaseError) as error:
                print(f"Error: {error}")
                self.output = None
                return None if fetch else False
            finally:
                conn.close()
            self.output = pd.DataFrame(value, columns=column_names)
            return self.output

class Locator:

    def __init__(self):
        self.locator = Nominatim(user_agent="https://maps.googleapis.com/")
    
    @cache
    def get_coords(self, location):
            location = self.locator.geocode(location, timeout=None)
            if location == None:
                return np.nan, np.nan
            return location.latitude, location.longitude

if __name__ == "__main__":
    query = 'SELECT name AS "region" FROM region'

    db = Database()
    df = db.execute(query)

    locator = Locator()
    with open(DATAPATH + "coords.csv", "w") as f:
        f.write("region,lat,lng\n")
        for i, value in enumerate(df[["region"]].values):
            print(f"\rCoordinates of region {i + 1} / {len(df)}", end="")
            lat, lng = locator.get_coords(value[0])
            f.write(f"\"{value[0]}\",{lat},{lng}\n")

