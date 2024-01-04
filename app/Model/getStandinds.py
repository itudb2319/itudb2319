from app.Model.database import db

def getSeasonStandings(year):
    return db.getData('seasonStandings.sql', {'yr': year})