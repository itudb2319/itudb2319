import psycopg2
import click, os
from flask.cli import with_appcontext
from os import path
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Database():
	def __init__(self, app) -> None:
		self.app = app
		self.db, self.cur = self.get_db()

	def insertCSV(self, tableCsvPaths: dict):
		for table, csvPath in tableCsvPaths.items():
			with open(csvPath, 'r') as f:
				copyQuery = f'COPY {table} FROM stdin WITH CSV HEADER NULL \'\\N\''

				self.cursor.copy_expert(sql=copyQuery, file=f)
				self.db.commit()
				print(f'{table} is inserted!')

	def get_db(self):
		self.db = psycopg2.connect(self.app.config['DB_URI'])
		self.cur = self.db.cursor()
		return self.db, self.cur

	def close_db(self):
		self.cur.close()
		self.db.close()

	def init_db(self):
		with open(path.join('queries', 'schema.sql')) as f:
			self.cur.execute(f.read())
			self.db.commit()

		try:
			PATH = 'data'

			tables = ['drivers', 'constructors', 'circuits', 'races', 'qualifying',
				'status', 'sprintResults', 'results', 'pitStops', 'lapTimes',
				'driverStandings', 'constructorStandings', 'constructorResults']
			
			tableCsvPaths = { table: os.path.join(PATH, table+'.csv') for table in tables }
			
			self.insertCSV(tableCsvPaths)

		except psycopg2.OperationalError as e:
			print(e)
			self.db.rollback()
			self.db.close()

		else:
			click.echo('Initialized the database.')

	@click.command('init-db')
	@with_appcontext
	def init_db_command(self):
		self.init_db()

	def init_app(self, app):
		app.teardown_appcontext(self.close_db)
		app.cli.add_command(self.init_db_command)

	def getRaceResults(self, params):
		with open(path.join('queries', 'raceResults.sql'), 'r') as f:
			query = f.read()
			
			try:
				self.cur.execute(query, vars=params)
				data = self.cur.fetchall()
			
			except psycopg2.OperationalError as e:
				print(e)
				self.db.rollback()
				self.db.close()

		return data

	def getRaceResults(self, params):
		with open(path.join('queries', 'raceResults.sql'), 'r') as f:
			query = f.read()
			
			try:
				self.cur.execute(query, vars=params)
				data = self.cur.fetchall()
			
			except psycopg2.OperationalError as e:
				print(e)
				self.db.rollback()
				self.db.close()

		return data

	def getLastRaceBestLaps(self):
		with open(path.join('queries', 'lastRaceLapTimes.sql'), 'r') as f:
			query = f.read()

			try:
				self.cur.execute(query, {'raceid': 1116})
				data = self.cur.fetchall()
			
			except psycopg2.OperationalError as e:
				print(e)
				self.db.rollback()
				self.db.close()

		return data

	def getDrivers(self):
		with open(path.join('queries', 'drivers.sql'), 'r') as f:
			query = f.read()

			try:
				self.cur.execute(query)
				data= self.cur.fetchall()

			except psycopg2.OperationalError as e:
				print(e)
				self.db.rollback()
				self.db.close()

		return data

	def getCircuits(self):
		with open(path.join('queries', 'circuits.sql'), 'r') as f:
			query = f.read()

			try:
				self.cur.execute(query)
				data= self.cur.fetchall()

			except psycopg2.OperationalError as e:
				print(e)
				self.db.rollback()
				self.db.close()

		return data

	def getSeasons(self, params):
		with open(path.join('queries', 'seasons.sql'), 'r') as f:
			query = f.read()

			try:
				self.cur.execute(query, params)
				data= self.cur.fetchall()

			except psycopg2.OperationalError as e:
				print(e)
				self.db.rollback()
				self.db.close()

		return data
		
	def getUsers(self):
		with open(path.join('queries', 'users.sql'), 'r') as f:
			query = f.read()

			try:
				self.cur.execute(query)
				data = self.cur.fetchall()
			except psycopg2.OperationalError as e:
				print(e)
				self.db.rollback()
				self.db.close()
		return data
