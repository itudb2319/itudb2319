from flask import Flask

from .Controller.gameBlink import gameBlinkBP
from .Controller.circuits import circuitsBP
from .Controller.contact import contactBP 
from .Controller.drivers import driversBP
from .Controller.quizzes import quizBP
from .Controller.raceResults import raceResultsBP
from .Controller.seasons import seasonsBP
from .Controller.auth import authBP
from .Controller.admin import adminBP
from .Controller.rankings import rankingsBP
from .Controller.constructors import constructorsBP

from app.Modal.database import db

def create_app():
    app = Flask('OnlyF1s', template_folder='templates', static_folder='static')
    app.secret_key = 'EECY'

    app.register_blueprint(authBP)
    app.register_blueprint(driversBP)
    app.register_blueprint(circuitsBP)
    app.register_blueprint(seasonsBP)
    app.register_blueprint(quizBP)
    app.register_blueprint(gameBlinkBP)
    app.register_blueprint(raceResultsBP)
    app.register_blueprint(contactBP)
    app.register_blueprint(adminBP)
    app.register_blueprint(rankingsBP)
    app.register_blueprint(constructorsBP)

    db.initDb()

    return app
