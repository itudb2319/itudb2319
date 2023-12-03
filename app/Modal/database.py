import psycopg2
from os.path import join, dirname, abspath
from os import environ

class Database:

    APP_PATH = dirname(abspath(__file__))
    DATA_PATH = join(dirname(APP_PATH), '..', 'data')
    QPATH = join(APP_PATH, 'queries')

    def __init__(self):
        self.conn = psycopg2.connect(
                    " user=" + environ.get('POSTGRES_USER') +\
                    " host=" + environ.get('POSTGRES_HOST') +\
                    " password=" + environ.get('POSTGRES_PASSWORD') +\
                    " dbname=" + environ.get('POSTGRES_DB')
        )
        self.cur = self.conn.cursor()

    def getDB(self):
        return self.conn, self.cur

    def closeDb(self):
        self.cur.close()
        self.conn.close()

    def initDb(self):
        with open(join(self.QPATH, 'schema_dev.sql')) as f:
            query = f.read()

        with self.conn:
            with self.cur:

                self.cur.execute("select * from information_schema.tables where table_name=%s", ('races',))
                created = self.cur.fetchall()
                if len(created) != 0:
                    self.cur.execute("select * from races LIMIT 5")
                    if len(self.cur.fetchall()) > 0: return
                
                self.cur.execute(query)
                self.conn.commit()

                tables = ['drivers', 'constructors', 'circuits', 'races', 'qualifying',
                          'status', 'sprintResults', 'results', 'pitStops', 'lapTimes',
                          'driverStandings', 'constructorStandings', 'constructorResults']

                tableCsvPaths = {table: join(self.DATA_PATH, table + '.csv') for table in tables}
                self.insertCSV(tableCsvPaths, self.cur, self.conn)

    def getData(self, queryFile, params):
        with open(join(self.QPATH, queryFile), 'r') as f:
            query = f.read()
            data = self.execute_query(query, params)
        return data

    def insertCSV(self, tableCsvPaths: dict, cursor, conn):
        PATHDIR = dirname(self.APP_PATH)
        for table, csvPath in tableCsvPaths.items():
            csvPathabs = join(PATHDIR, 'data', csvPath)
            with open(csvPathabs, 'r') as f:
                copyQuery = f'COPY {table} FROM stdin WITH CSV HEADER NULL \'\\N\''

                cursor.copy_expert(sql=copyQuery, file=f)
                conn.commit()
                print(f'{table} is inserted!')

    def execute_query(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            data = cur.fetchall()
        return data

db = Database()