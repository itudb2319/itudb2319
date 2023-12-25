from .database import db
from os.path import join

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