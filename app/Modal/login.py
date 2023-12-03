from app.Modal.database import db

def login(self, username, password):
    return db.getData('auth.sql', {'username': username, 'password': password})