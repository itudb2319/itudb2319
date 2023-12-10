from .database import db
from os.path import join

def getConstructors():
    with open(join(db.QPATH, 'constructors.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query)
    return data