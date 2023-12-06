from app.Modal.database import db
from os.path import join

def getCircuits():
    with open(join(db.QPATH, 'circuits.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query)
    return data
