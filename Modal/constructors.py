from .database import db
from os.path import join

def getConstructors():
    with open(join(db.QPATH, 'constructors.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query)
    return data

def getConstructorDriver(params):
    with open(join(db.QPATH, 'constructorDriver.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query, params)

    return data

def getConstructorCircuit(params):
    with open(join(db.QPATH, 'constructorCircuit.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query, params)

    return data
