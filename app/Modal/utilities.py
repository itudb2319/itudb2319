from .database import db
import re

def columnTypesWithNames(columnDisplay, tableName):
    columnListQuery =   f"""
                            SELECT  attname            AS col,
                                    atttypid::regtype  AS datatype
                            FROM    pg_attribute
                            WHERE   attrelid = 'public.{tableName}'::regclass
                            AND     attnum > 0
                            AND     NOT attisdropped
                            AND     attname IN (
                        """
    
    for i, columnNames in enumerate(columnDisplay):
        if i != len(columnDisplay)-1:
            columnListQuery += f"'{columnNames}', "
        else:
            columnListQuery += f"'{columnNames}') "

    columnListQuery += "ORDER BY CASE "

    for i, columnNames in enumerate(columnDisplay):
        columnListQuery += f"WHEN attname = '{columnNames}' THEN {i} "

    columnListQuery += "END"
    return db.executeQuery(columnListQuery)

def genericDataPrinter(tableName, id, columnDisplay, limitter, search=None, orderBy=None):

    columnList = columnTypesWithNames(columnDisplay, tableName)
    columns = ""
    for i, element in enumerate(columnList):
        if i != len(columnList) - 1:
            columns += (element[0] + ', ')
        else:
            columns += (element[0])

    query = f"SELECT {id}, {columns} FROM {tableName} WHERE "

    if search:
        if search == "None":
            for i, (columnName, columnType) in enumerate(columnList):
                query += f"{columnName} is null"
                if i != len(columnList) -1:
                    query += " OR "
        
        else: 
            timeFlag = re.search(":", search) or re.search("\+", search)
            dateFlag = re.search("-", search)
            websiteFlag = re.search("http", search)

            for i, (columnName, columnType) in enumerate(columnList):
                if (re.search("int", columnType) or re.search("numeric", columnType)):
                    if (re.findall(r'(?<![0-9:.])\b\d+.\d+\b(?![0-9:.])', search) or search.isdigit()):
                        query += f"{columnName} = {search} OR "

                elif (re.search("time", columnType)):
                    if timeFlag:
                        query += f"{columnName} = '{search}' OR "

                elif (re.search("date", columnType)):
                    if dateFlag:
                        query += f"{columnName} = '{search}' OR "

                else:
                    query += f"{columnName} ILIKE '%{search}%' OR "

            if query[-4:] == " OR ":
                query = query[:-4]

    else:
        query += " true"

    if orderBy:
        query += f" ORDER BY {orderBy}"

    if limitter == 'all':
        pass
    else:
        if limitter != "":
            query += f" LIMIT {limitter}"

    query = query.replace(";", "")
    query = query.replace("--", "")

    data = db.executeQuery(query)
    return data

def parseForms(requestForm):
    showList = list()
    orderBy = ""
    search = ""
    deletedElementIdList = list()
    deletedElementTableName = ""
    deletedElementId = ""
    updatedElementList = list()
    insertedElementList = list()
    limitter = ""
    for key, value in requestForm:
        if value == 'show':
            showList.append(key)
        elif key == 'orderBy':
            orderBy = value
        elif key == 'search':
            search = value
        elif value == 'checkboxDelete':
            deletedElementIdList.append(key.split("_")[2])
            deletedElementTableName = key.split("_")[0]
            deletedElementId = key.split("_")[1]
        elif value =="updateElement":
            updatedElementList.append((key.split("_")[0], key.split("_")[1], key.split("_")[2]))
        elif value =="insertElements":
            insertedElementList.append((key.split("_")[0], key.split("_")[1]))
        elif key =="limitter":
            limitter = value
    if len(updatedElementList) > 0:
        updatedElementList.pop(0)
    return showList, orderBy, search, deletedElementIdList, deletedElementTableName, deletedElementId, updatedElementList, insertedElementList, limitter

def getResults(tableName, limit=100):
    return db.executeQuery(f"SELECT * FROM {tableName} LIMIT {limit};")

def getColumns(tableName, id):
    query = f"""
                SELECT attname AS col
                FROM   pg_attribute
                WHERE  attrelid = 'public.{tableName}'::regclass AND attname != '{id}'
                AND    attnum > 0
                AND    NOT attisdropped
                ORDER  BY attnum
            """
    result = db.executeQuery(query)
    return [e[0] for e in result]
    
def getIds(id, tableName):
    return db.executeQuery(f"SELECT {id} FROM {tableName}")

def getPrimary(tableName):
    return db.executeQuery(f"""
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                            AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = '{tableName}'::regclass
        AND    i.indisprimary;
""")

def deleteElementsFromTable(tableName, tableId, idList):
    idString = ', '.join(f"{item}" for item in idList)

    query = f"DELETE FROM {tableName} WHERE {tableId} IN ({idString})"

    db.executeBulkQuery(query, commit=1)
    
def updateElements(tableName, updateElementList, id):
    myColumns = []
    for element in updateElementList:
        myColumns.append(element[0])

    columnList = columnTypesWithNames(myColumns, tableName)

    query = f"UPDATE {tableName} SET "
    primaryKey = getPrimary(tableName)[0][0]

    for i in range(len(columnList)):
        if (updateElementList[i][1] == ''):
            query += f"{columnList[i][0]} = NULL"
        elif (re.search("int", columnList[i][1]) or re.search("numeric", columnList[i][1])):
            query += f"{columnList[i][0]} = {updateElementList[i][1]}"
        else:
            query += f"{columnList[i][0]} = '{updateElementList[i][1]}'"

        if i != len(columnList) -1:
            query+= " , "

    query += f" WHERE {primaryKey} = {updateElementList[0][2]}"
    
    db.executeBulkQuery(query)


def deleteElementsFromTable(tableName, tableId, idList):
    idString = ', '.join(f"{item}" for item in idList)

    query = f"DELETE FROM {tableName} WHERE {tableId} IN ({idString})"

    db.executeBulkQuery(query, commit=1)


def insertElementToTable(tableName, insertedElementList):
    keyStr = ""
    keyList = list()
    for element in insertedElementList:
        keyList.append(element[0])

    keyStr = ', '.join(f"{item}" for item in keyList)


    myColumns = []
    for element in insertedElementList:
        myColumns.append(element[0])

    columnList = columnTypesWithNames(myColumns, tableName)

    query = f"INSERT INTO {tableName} ({keyStr}) VALUES ("
    params = []
    for i in range(len(columnList)):
        if (insertedElementList[i][1] == ''):
            query += f"NULL"
        elif (re.search("int", columnList[i][1]) or re.search("numeric", columnList[i][1])):
            params.append(insertedElementList[i][1])
            query += f" %s "
        else:
            params.append(insertedElementList[i][1])
            query += f"%s"

        if i != len(columnList) -1:
            query+= " , "

    query += ")"
    db.executeBulkQuery(query, params=params, commit=1)