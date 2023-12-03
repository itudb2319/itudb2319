from .database import db
from os.path import join

def getDrivers():
    with open(join(db.QPATH, 'drivers.sql'), 'r') as f:
        query = f.read()
        data = db.execute_query(query)
    return data
    
def getFilteredDrivers(filtered_columns):
		cond = ', '.join(filtered_columns)
		header_cond = ", ".join([f"'{item}'" for item in filtered_columns])
		data = db.execute_query(f"SELECT driverId, {cond} FROM drivers;")
		return data
