import psycopg2
from psycopg2.extras import DictCursor, RealDictCursor
import click
from flask import current_app
from os.path import join, dirname, abspath
from os import chdir

APP_PATH = dirname(abspath(__file__))
DATA_PATH = join(dirname(APP_PATH), 'data')
QPATH = join(APP_PATH, 'queries')

class Database():
	def __init__(self, app):
		self.app = app
		self.getDB()

	def getDB(self):
		self.conn = psycopg2.connect(self.app.config['DB_URI'], cursor_factory=DictCursor)
		self.cur = self.conn.cursor()
		return self.conn, self.cur
	
	def getData(self, queryFile, params):
		with open(join(QPATH, queryFile), 'r') as f:
			query = f.read()
			
			try:
				self.cur.execute(query, vars=params)
				data = self.cur.fetchall()
			
			except psycopg2.OperationalError as e:
				click(e)
				self.conn.rollback()
				self.conn.close()

		return data
	
	def addData(self, queryFile, params):
		with open(join(QPATH, queryFile), 'r') as f:
			query = f.read()
			
			try:
				self.cur.execute(query, vars=params)
			
			except psycopg2.OperationalError as e:
				click(e)
				self.conn.rollback()
				self.conn.close()

		return

	def getRaceResults(self, params):
		return self.getData('raceResults.sql', params)

	def getLastRaceBestLaps(self):
		return self.getData('lastRaceLapTimes.sql', {'raceid': 1116})
		# raceid given manually because last race have no records in laptimes
	
	def getDrivers(self):
		with open(join(QPATH, 'drivers.sql'), 'r') as f:
			query = f.read()

			try:
				self.cur.execute(query)
				data = self.cur.fetchall()

			except psycopg2.OperationalError as e:
				click(e)
				self.conn.rollback()
				self.conn.close()

		return data

	def getCircuits(self):
		with open(join(QPATH, 'circuits.sql'), 'r') as f:
			query = f.read()

			try:
				self.cur.execute(query)
				data = self.cur.fetchall()

			except psycopg2.OperationalError as e:
				click(e)
				self.conn.rollback()
				self.conn.close()

		return data

	def getSeasons(self, params):
		with open(join(QPATH, 'seasons.sql'), 'r') as f:
			query = f.read()

			try:
				self.cur.execute(query, params)
				data = self.cur.fetchall()

			except psycopg2.OperationalError as e:
				click(e)
				self.conn.rollback()
				self.conn.close()

		return data
		
	def login(self, username, password):
		return self.getData('auth.sql', {'username': username, 'password': password})
	
	def signUp(self, username, password):
		return self.addData('userSignUp.sql', {'username': username, 'password': password})
	
	def userCheck(self, username, password):
		count = self.getData('userCheck.sql', {'username': username, 'password': password})
		return count == 0

def insertCSV(tableCsvPaths: dict, cursor, conn):
	PATHDIR = dirname(APP_PATH)
	for table, csvPath in tableCsvPaths.items():
		csvPathabs = join(PATHDIR, 'data', csvPath)
		with open(csvPathabs, 'r') as f:
			copyQuery = f'COPY {table} FROM stdin WITH CSV HEADER NULL \'\\N\''

			cursor.copy_expert(sql=copyQuery, file=f)
			conn.commit()
			print(f'{table} is inserted!')

def init_db():
	with open(join(QPATH, 'schema_dev.sql')) as f:
		query = f.read()

	try:
		conn = psycopg2.connect(current_app.config['DB_URI'])
		cur = conn.cursor()

		# check if the db is already initialized
		cur.execute("select * from information_schema.tables where table_name=%s", ('races',))
		created = cur.fetchall()
		if len(created) != 0:
			cur.execute("select * from races LIMIT 5")
			if len(cur.fetchall()) > 0: return
		
		cur.execute(query)
		conn.commit()

		tables = ['drivers', 'constructors', 'circuits', 'races', 'qualifying',
			'status', 'sprintResults', 'results', 'pitStops', 'lapTimes',
			'driverStandings', 'constructorStandings', 'constructorResults']
		
		tableCsvPaths = {table: join(DATA_PATH, table+'.csv') for table in tables}
		
		insertCSV(tableCsvPaths, cur, conn)

	except psycopg2.OperationalError as e:
		click(e)
		conn.rollback()

	else:
		click.echo('Initialized the database.')
	
	finally:
		cur.close()
		conn.close()

