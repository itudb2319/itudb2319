from .database import db
from os.path import join

def getDrivers():
    with open(join(db.QPATH, 'drivers.sql'), 'r') as f:
        query = f.read()
        
        data = db.execute_query(query)
    return data
