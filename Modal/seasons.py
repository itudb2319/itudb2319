from app.Modal.database import db
from os.path import join

def getSeasons(params):
    with open(join(db.QPATH, 'seasons.sql'), 'r') as f:
        query = f.read()
        data = db.executeQuery(query, params)
    return data
