from app.Modal.database import db

def getRaceResults(params):
    return db.getData('raceResults.sql', params)

def getLastRaceBestLaps():
    return db.getData('lastRaceLapTimes.sql', {'raceid': 1116})
    # raceId should be determined dynamically
    # raceid given manually because last race have no records in laptimes