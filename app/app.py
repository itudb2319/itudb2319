from flask import Flask, render_template, current_app
from database import Database, init_db
import argparse
from blueprints import authBP, driversBP, circuitsBP, seasonsBP, quizBP, gameBlinkBP, raceResultsBP, contactBP
import os

app = Flask('OnlyF1s', template_folder='templates', static_folder='static')
app.register_blueprint(authBP)
app.register_blueprint(driversBP)
app.register_blueprint(circuitsBP)
app.register_blueprint(seasonsBP)
app.register_blueprint(quizBP)
app.register_blueprint(gameBlinkBP)
app.register_blueprint(raceResultsBP)
app.register_blueprint(contactBP)


parser = argparse.ArgumentParser(
                    prog='OnlyF1s',
                    description='Flask App for F1',
                    epilog='You should provide password for with cloud -c')

parser.add_argument('-c', '--cloud', action='store_true')
parser.add_argument('-i', '--init_db', action='store_true')
args = parser.parse_args()

if args.cloud and not args.password:
    raise AttributeError('You should provide password for with cloud -c')

if not args.cloud:
	app.debug = True
	app.config['DB_URI'] = os.environ['DB_LOCAL'][1:-1]
	# app.config['DB_URI'] = "host=db port=5432 user=postgres dbname=postgres password=postgres"

else:
	app.debug = False
	app.config['DB_URI'] = os.environ['DB'] % args.password

@app.route('/')
def index():
	data = dict()
	data['caption_text'] = 'Last Race Lap Times for Drivers'
	data['titles'] = ['Circuit', 'Lap', 'Time', 'Name', 'Nationality']
	data['context'] = current_app.db.getLastRaceBestLaps()
	return render_template('index.html', context=data)

if __name__ == "__main__":
	if args.init_db:
		with app.app_context():
			init_db()
	
	with app.app_context():
		current_app.db = Database(app)


	app.run(host="0.0.0.0", port=8000, debug=True)
