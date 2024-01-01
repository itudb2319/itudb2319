from flask import Flask
from app.Modal.database import db
from .Modal.mail_setup import mail

db.initDb()


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
from .Controller.standings import standingsBP
from .Controller.results import resultsBP
from .Controller.sprintResults import sprintResultsBP
from .Controller.qualifying import qualifyingBP
from .Controller.driverStandings import driverStandingsBP
from .Controller.pitStops import pitStopsBP
from .Controller.status import statusBP
from .Controller.constructorStandings import constructorStandingsBP
from .Controller.races import racesBP
from .Controller.constructorResults import constructorResultsBP
from .Controller.lapTimes import laptimesBP

def create_app():
    app = Flask('OnlyF1s', template_folder='templates', static_folder='static')
    app.secret_key = 'EECY'

    app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'c9b637e184221e'
    app.config['MAIL_PASSWORD'] = '00a75064ea9f59'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mail.init_app(app)
    app.register_blueprint(standingsBP)
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
    app.register_blueprint(resultsBP)
    app.register_blueprint(sprintResultsBP)
    app.register_blueprint(qualifyingBP)
    app.register_blueprint(driverStandingsBP)
    app.register_blueprint(pitStopsBP)
    app.register_blueprint(statusBP)
    app.register_blueprint(constructorStandingsBP)
    app.register_blueprint(laptimesBP)
    app.register_blueprint(racesBP)
    app.register_blueprint(constructorResultsBP)

    return app
