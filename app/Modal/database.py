import psycopg2
from os.path import join, dirname, abspath
from os import environ
import csv, re

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

    def initDb(self):
        with open(join(self.QPATH, 'schema_dev.sql')) as f:
            query = f.read()


        created = self.executeQuery("SELECT * FROM information_schema.tables WHERE table_name=%s", params=('races',))
        if len(created) != 0:
            if len(self.executeQuery("SELECT * FROM races LIMIT 5")) > 0: return
        
        self.executeQuery(query, commit=1)

        tables = ['drivers', 'constructors', 'circuits', 'races', 'qualifying',
                    'status', 'sprintResults', 'results', 'pitStops', 'lapTimes',
                    'driverStandings', 'constructorStandings', 'constructorResults']

        tableCsvPaths = {table: join(self.DATA_PATH, table + '.csv') for table in tables}
        self.insertCSV(tableCsvPaths, self.conn.cursor( ), self.conn)

    def getData(self, queryFile, params):
        with open(join(self.QPATH, queryFile), 'r') as f:
            query = f.read()
            data = self.executeQuery(query, params)
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

    def executeQuery(self, query, params=None, getData=0, commit=0):
        self.cur = self.conn.cursor()
        data = None

        try:
            self.cur.execute(query, params)
            if commit == 1:
                self.conn.commit()
                self.cur.close()
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
                self.cur.close()
        except psycopg2.Error as Error:
            self.conn.rollback()
            raise ValueError(f"""An error has been occured --> {Error}\nThis is the query:\n\t{query}""")

    def generateQuery(self,filename):
        self.__init__()
        filename = join("/project/app/uploads", filename)
        pattern = r'(\d+)(\w+)\.(\w+)'
        parsedResult = re.search(pattern, filename)
        table_id = None; operation = None; fileExtension = None
        if parsedResult:
            tableId = parsedResult.group(1)
            operation = parsedResult.group(2)
            fileExtension = parsedResult.group(3)
        else:
            return -1
        
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            rowCount = sum(1 for row in file)
        
        tableName = self.executeQuery(f"SELECT tableName FROM lkp_tables WHERE tableId = {tableId};", getData=1)
        match operation:
            case "UP":
                primaryColumns = self.executeQuery(f"""SELECT a.attname
                                                        FROM
                                                            pg_class AS c
                                                            JOIN pg_index AS i ON c.oid = i.indrelid AND i.indisprimary
                                                            JOIN pg_attribute AS a ON c.oid = a.attrelid AND a.attnum = ANY(i.indkey)
                                                        WHERE c.oid = '{tableName}'::regclass;"""
                                                    )
                primaryColumns = [', '.join(map(str, row)) for row in primaryColumns]
                pkNumber = len(primaryColumns)
                queryPairs = {}
                primaryKeys = []

                with open(filename, 'r') as file:
                    reader = csv.reader(file)
                    for i, row in enumerate(reader):
                        queryPairs = {}
                        primaryKeys = []

                        colvalPairs = []
                        primaryKeys = row[0].split('+')
                        colvalPairs = row[1].split('-')
                        for pair in colvalPairs:  
                            key = pair.split(':')[0]
                            value = pair.split(':')[1]
                            queryPairs.update({key:value})

                        updatedColumnNumber = len(queryPairs)
                        query = f"UPDATE {tableName}\nSET\n"
                        for j, (key, value) in enumerate(queryPairs.items()):
                            query += f"\t{key} = {value}"
                            if j != updatedColumnNumber-1:
                                query += ",\n"
                            
                        query += "\nWHERE"
                        for k, (pc, pk) in enumerate(zip(primaryColumns, primaryKeys)):
                            query += f" {pc} = {pk}"
                            if k != pkNumber-1:
                                query += " AND"
                        query += ";"
                        if i != rowCount - 1:
                            self.executeBulkQuery(query)
                        else:
                            self.executeBulkQuery(query, commit=1)

            case "IN":
                with open(filename, 'r') as file:
                    reader = csv.reader(file)

                    for i, row in enumerate(reader):
                        queryPairs = {}		
                        
                        colvalPairs = row[0].split('-')
                        for pair in colvalPairs:  
                            key = pair.split(':')[0]
                            value = pair.split(':')[1]
                            queryPairs.update({key:value})

                        columnNumber = len(queryPairs)
                        query = f"INSERT INTO {tableName}("
                        for j, key in enumerate(queryPairs.keys()):
                            query += key
                            if j != columnNumber-1:
                                query += ", "

                        query += ")\nVALUES("
                        for i, value in enumerate(queryPairs.values()):
                            query += f"{value}"
                            if i != columnNumber-1:
                                query += ", "
                        
                        query += ");"
                        if i != rowCount-1:
                            self.executeBulkQuery(query)
                        else:
                            self.executeBulkQuery(query, commit=1)

            
            case "DEL":
                primaryColumns = self.executeQuery(f"""SELECT a.attname
                                                        FROM
                                                            pg_class AS c
                                                            JOIN pg_index AS i ON c.oid = i.indrelid AND i.indisprimary
                                                            JOIN pg_attribute AS a ON c.oid = a.attrelid AND a.attnum = ANY(i.indkey)
                                                        WHERE c.oid = '{tableName}'::regclass;"""
                                                    )
                primaryColumns = [', '.join(map(str, row)) for row in primaryColumns]
                pkNumber = len(primaryColumns)
                primaryKeys = []
                with open(filename, 'r') as file:
                    reader = csv.reader(file)
                    for i, row in enumerate(reader):
                        primaryKeys = row[0].split('+')

                        query = f"DELETE FROM {tableName} WHERE\n\t"
                        for j, (pc, pk) in enumerate(zip(primaryColumns, primaryKeys)):
                            query += f"{pc} = {pk}"
                            if j != pkNumber-1:
                                query += " AND "
                            
                        query += ";"
                        if i != rowCount-1:
                            self.executeBulkQuery(query)
                        else:
                            self.executeBulkQuery(query, commit=1)
            
            case _:
                return -1
        

db = Database()
