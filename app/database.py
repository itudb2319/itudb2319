import psycopg2
import click, os
from flask import current_app, g
from flask.cli import with_appcontext
from os import path
import os

PATH = path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Database():
	def __init__(self, app) -> None:
		self.app = app
		self.db, self.cur = self.get_db()

	def get_db(self):
		self.db = psycopg2.connect(self.app.config['DB_URI'])
		self.cur = self.db.cursor()
		return self.db, self.cur

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


def insertCSV(tableCsvPaths: dict, cursor, db):
	PATHDIR = path.dirname(PATH)
	for table, csvPath in tableCsvPaths.items():
		csvPathabs = path.join(PATHDIR, 'data', csvPath)
		with open(csvPathabs, 'r') as f:
			copyQuery = f'COPY {table} FROM stdin WITH CSV HEADER NULL \'\\N\''

			cursor.copy_expert(sql=copyQuery, file=f)
			db.commit()
			print(f'{table} is inserted!')

def init_db():
	with open(path.join(PATH, 'queries', 'schema_dev.sql')) as f:
		query = f.read()

	try:
		db = psycopg2.connect(current_app.config['DB_URI'])
		
		cur = db.cursor()
		cur.execute("select * from information_schema.tables where table_name=%s", ('races',))
		k = cur.fetchall()
		print(k, 'here1')
		if len(k) != 0:
			cur.execute("select * from races LIMIT 5")
			res = cur.fetchall()
			if len(res) != 0:
				print(res, 'here2')
				return
		print('Final')
		cur.execute(query)
		db.commit()

		tables = ['drivers', 'constructors', 'circuits', 'races', 'qualifying',
			'status', 'sprintResults', 'results', 'pitStops', 'lapTimes',
			'driverStandings', 'constructorStandings', 'constructorResults']
		
		tableCsvPaths = { table: os.path.join(table+'.csv') for table in tables }
		
		insertCSV(tableCsvPaths, cur, db)

	except psycopg2.OperationalError as e:
		print(e)
		db.rollback()
		db.close()

	else:
		click.echo('Initialized the database.')

