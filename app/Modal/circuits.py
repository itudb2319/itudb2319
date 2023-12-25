from .database import db
from os.path import join

from .database import db
from os.path import join

columnDict = {"name": "Name",
        "location": "Location",
        "country": "Country",
        "circuitRef": "Reference", 
        }

def getCircuits(columnList, orderBy, search):
    columns = ', '.join(map(str, columnList))
    query = f"SELECT {columns} FROM circuits"

    if search != "":
        query += " WHERE"
        for item in columnList:
            query += f" {item} = '{search}' OR {item} ILIKE '%{search}%' OR"
        query = query[:-3]

    if orderBy != "":
        query +=  f" ORDER BY {orderBy}"
    
    print(query)
    data = db.executeQuery(query)
    return data