from app.Modal.database import db
from psycopg2 import IntegrityError

def getUser(username, password):
    user = db.getData('login.sql', {'username': username, 'psw': password})
    print(user)
    if len(user) == 0:
        return None
    else: return user[0]

def registerUser(username, password):
    error = None
    try:
        if db.cur is None or db.cur.closed: db.cur = db.conn.cursor()
        db.cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        db.conn.commit()
    except IntegrityError:
        error = f"User {username} is already registered."

    return error