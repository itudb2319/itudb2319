import psycopg2
from os.path import join, dirname, abspath
from os import environ

class Database:

    APP_PATH = dirname(abspath(__file__))
    DATA_PATH = join(dirname(APP_PATH), '..', 'data')
    QPATH = join(APP_PATH, 'queries')

    def __init__(self):
        self.conn = psycopg2.connect(
                    user = environ.get('POSTGRES_USER'),
                    host = environ.get('POSTGRES_HOST'),
                    password = environ.get('POSTGRES_PASSWORD'),
                    dbname = environ.get('POSTGRES_DB')
        )
        self.cur = self.conn.cursor()

    def refreshDatabaseConnection(self):
        self.conn.close()
        self.conn = psycopg2.connect(
                    user = environ.get('POSTGRES_USER'),
                    host = environ.get('POSTGRES_HOST'),
                    password = environ.get('POSTGRES_PASSWORD'),
                    dbname = environ.get('POSTGRES_DB')
        )

    def initDb(self):
        with open(join(self.QPATH, 'schemaDev.sql')) as f:
            query = f.read()

        # Check whether DB is already initialized
        created = self.executeQuery("SELECT * FROM information_schema.tables WHERE table_name=%s", params=('races',))
        if len(created) != 0:
            if len(self.executeQuery("SELECT * FROM races LIMIT 5")) > 0: return
        
        self.executeQuery(query, commit=1)
        self.refreshDatabaseConnection()

        # Create admin role
        from ..Modal.authHelper import registerUser
        from werkzeug.security import generate_password_hash
        registerUser('admin', generate_password_hash('123'), role=1)

        tables = ['drivers', 'constructors', 'circuits', 'races', 'qualifying',
                    'status', 'sprintResults', 'results', 'pitStops', 'lapTimes',
                    'driverStandings', 'constructorStandings', 'constructorResults']

        tableCsvPaths = {table: join(self.DATA_PATH, table + '.csv') for table in tables}
        self.insertCSV(tableCsvPaths, self.conn.cursor( ), self.conn)

    def insertCSV(self, tableCsvPaths: dict, cursor, conn):
        PATHDIR = dirname(self.APP_PATH)
        for table, csvPath in tableCsvPaths.items():
            csvPathabs = join(PATHDIR, 'data', csvPath)
            with open(csvPathabs, 'r') as f:
                copyQuery = f'COPY {table} FROM stdin WITH CSV HEADER NULL \'\\N\''

                cursor.copy_expert(sql=copyQuery, file=f)
                conn.commit()
                print(f'{table} is inserted!')

    def getData(self, queryFile, params):
        with open(join(self.QPATH, queryFile), 'r') as f:
            query = f.read()
            data = self.executeQuery(query, params)
        return data

    def executeQuery(self, query, params=None, getData=0, commit=0):
        self.cur = self.conn.cursor()
        data = None

        try:
            self.cur.execute(query, params)
            if commit == 1:
                self.conn.commit()
                self.refreshDatabaseConnection()
                return
            else:
                if getData == 1:
                    data = self.cur.fetchone()
                    if data is not None:
                        data = data[0]
                else:
                    data = self.cur.fetchall()
        except psycopg2.Error as Error:
            self.conn.rollback()
            raise ValueError(f"""An error has been occured --> {Error}\nThis is the query:\n\t{query}""")
        finally:
            self.cur.close()
            return data
        
    def executeBulkQuery(self, query, params=None, commit=0):
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(query, params)
            if commit == 1:
                self.conn.commit()
                self.refreshDatabaseConnection()
        except psycopg2.Error as Error:
            self.conn.rollback()
            raise ValueError(f"""An error has been occured --> {Error}\nThis is the query:\n\t{query}""")

db = Database()
