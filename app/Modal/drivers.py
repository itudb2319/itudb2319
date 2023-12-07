from .database import db
from os.path import join

columnDict = {
            "driverId": "ID",
            "forename": "Name",
            "surname": "Surname",
            "nationality": "Nationality",
            "number": "Number",
            "driverRef": "Reference", 
            "code": "Code",
            "dob": "Date of Birth"
            }
    
defaultList = ["ID", "Name", "Surname", "Nationality", "Number"]
defaultListKeys = ["driverId", "forename", "surname", "nationality", "number"]

def getDrivers(columnList, orderBy = ""):
    columns = ', '.join(map(str, columnList))
    if orderBy != "":
        data = db.executeQuery(f"SELECT {columns} FROM drivers ORDER BY {orderBy}")
    else:
        data = db.executeQuery(f"SELECT {columns} FROM drivers")
    return data