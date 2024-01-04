from app.Model.database import db
from os.path import join

def getRankings(rankingName, params):
    sqlfile = f"{rankingName}.sql"

    with open(join(db.QPATH, sqlfile), 'r') as f:
        query = f.read()
        data = db.executeQuery(query, params)
    return data

def getHeadersForRanking(rankingName):
    header_mapping = {
        'totalEntries': ['Name', 'Surname', 'Count'],
        'youngestEntries': ['Name', 'Surname', 'Age', 'Race', 'Season', 'Round', 'Result'],
        'oldestEntries': ['Name', 'Surname', 'Age', 'Race', 'Season', 'Round', 'Result'],
        'youngestFinish': ['Name', 'Surname', 'Age', 'Race', 'Season', 'Round', 'Result'],
        'oldestFinish': ['Name', 'Surname', 'Age', 'Race', 'Season', 'Round', 'Result'],
        'totalWins': ['Name', 'Surname', 'Seasons', 'Entries', 'Wins', '%'],
        'perWins': ['Name', 'Surname', 'Seasons', 'Entries', 'Wins', '%'],
        'youngestWins': ['Name', 'Surname', 'Age', 'Season', 'Race'],
        'oldestWins': ['Name', 'Surname', 'Age', 'Season', 'Race']
    }
    return header_mapping.get(rankingName, [])
