from .database import db
from os.path import join

def getDrivers():
    with open(join(db.QPATH, 'drivers.sql'), 'r') as f:
        query = f.read()
        
        data = db.execute_query(query)
    return data
    
def getFilteredDrivers(self, filtered_columns):
		cond = ', '.join(filtered_columns)
		header_cond = ", ".join([f"'{item}'" for item in filtered_columns])
		try:
			self.cur.execute(f"SELECT driverId, {cond} FROM drivers;")
			data = self.cur.fetchall()

		except psycopg2.OperationalError as e:
			click(e)
			self.conn.rollback()
			self.conn.close()

		return data
