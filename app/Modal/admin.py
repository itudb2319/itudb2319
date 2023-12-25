from .database import db
from .utilities import getPrimary, columnTypesWithNames
from os.path import join
import re
import csv

def generateQuery(filename):
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
        
        tableName = db.executeQuery(f"SELECT tableName FROM lkp_tables WHERE tableId = {tableId};", getData=1)
        match operation:
            case "UP":
                primaryColumns = db.executeQuery(f"""SELECT a.attname
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
                            db.executeBulkQuery(query)
                        else:
                            db.executeBulkQuery(query, commit=1)

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
                            db.executeBulkQuery(query)
                        else:
                            db.executeBulkQuery(query, commit=1)

            
            case "DEL":
                primaryColumns = db.executeQuery(f"""SELECT a.attname
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
                            db.executeBulkQuery(query)
                        else:
                            db.executeBulkQuery(query, commit=1)
            
            case _:
                return -1
