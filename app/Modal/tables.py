from app.Modal.database import db
from os.path import join


def getTables():
    with open(join(db.QPATH, 'tables.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query)
    return data