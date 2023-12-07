from .database import db
from os.path import join

from .database import db
from os.path import join

columnDict = {"circuitId": "ID",
        "name": "Name",
        "location": "Location",
        "country": "Country",
        "circuitRef": "Reference", 
        "lat": "Latitude",
        "lng": "Longitude",
        "alt": "Altitude"
        }

defaultList = ["ID", "Name", "Location", "Country", "Reference"]
defaultListKeys = ["circuitId", "name", "location", "country", "circuitRef"]

def getCircuits(columnList, orderBy = ""):
    columns = ', '.join(map(str, columnList))
    if orderBy != "":
        data = db.executeQuery(f"SELECT {columns} FROM circuits ORDER BY {orderBy}")
    else:
        data = db.executeQuery(f"SELECT {columns} FROM circuits")
    return data