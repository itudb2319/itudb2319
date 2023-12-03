from flask import Flask

from .Controller.gameBlink import gameBlinkBP
from .Controller.circuits import circuitsBP
from .Controller.contact import contactBP 
from .Controller.drivers import driversBP
from .Controller.quizzes import quizBP
from .Controller.raceResults import raceResultsBP
from .Controller.seasons import seasonsBP
from .Controller.auth import authBP

from app.Modal.database import db

def create_app():
    app = Flask('OnlyF1s', template_folder='templates', static_folder='static')

    app.register_blueprint(authBP)
    app.register_blueprint(driversBP)
    app.register_blueprint(circuitsBP)
    app.register_blueprint(seasonsBP)
    app.register_blueprint(quizBP)
    app.register_blueprint(gameBlinkBP)
    app.register_blueprint(raceResultsBP)
    app.register_blueprint(contactBP)

    db.initDb()

    return app
