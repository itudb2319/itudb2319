from .database import db
from os.path import join

columnDict = {
            "forename": "Name",
            "surname": "Surname",
            "nationality": "Nationality",
            "number": "Number",
            }

def getDrivers(columnList, orderBy, search, page):
    columns = ', '.join(map(str, columnList))

    query = f"SELECT {columns} FROM drivers"
    if search != "":
        query += " WHERE"
        if len(search.split()) == 1:
                for item in columnDict:
                    if item != "number" and item != "dob":
                        query += f" {item} = '{search}' OR {item} ILIKE '%{search}%' OR"
                    elif item == "number" and search.isdigit():
                        query += f" {item} = {search} OR"
                query = query[:-3]
        elif len(search.split()) == 2:
            name = search.split()[0]
            surname = search.split()[1]
            query += f" (forename = '{name}' OR forename ILIKE '%{name}%') AND (surname = '{surname}' OR surname ILIKE '%{surname}%')"

    if orderBy != "":
        query +=  f" ORDER BY {orderBy}"
    data = db.executeQuery(query)
    length = len(data)
    if (search != ""):
         query += f" LIMIT 20"
    else:
        query += f" LIMIT 20 OFFSET {(int(page) - 1) * 20}"
    print(query)
    data = db.executeQuery(query)
    return data, length

def getDriverPersonal(params):
    with open(join(db.QPATH, 'personalDetails.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query, params)
    return data

def getDriverCareer(params):
    with open(join(db.QPATH, 'careerDetails.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query, params)
    return data

