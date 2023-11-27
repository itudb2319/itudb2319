from flask import Flask, request, render_template
from database import Database
import os

app = Flask(__name__, template_folder='templates')

ENV = 'dev'
if ENV == 'dev':
	app.debug = True
	app.config['DB_URI'] = os.environ['DEV_DB']
	# app.config['DB_URI'] = "dbname=f1 user=root"
else:
	app.debug = False
	app.config['DB_URI'] = os.environ['DB']

db = Database(app)

@app.route('/')
def index():
	data = dict()
	data['caption_text'] = 'Last Race Lap Times for Drivers'
	data['titles'] = ['Circuit', 'Lap', 'Time', 'Name', 'Nationality']
	data['context'] = db.getLastRaceBestLaps()
	return render_template('index.html', context=data)

@app.route('/raceResults', methods=['GET', 'POST'])
def raceResults():
	titles=["Name", "Surname", "Nationality", "No.", "Circuit name", "Year", "fastest lap", "position", "position text*"]
	
	if request.method == 'POST':
		raceYear = request.form.get('raceYear', default=None, type=str) or None
		respNumber = request.form.get('respNumber', default=None, type=int)
		circuitRef = request.form.get('circuitRef', default='', type=str).lower()
		
		params = {'raceYear': raceYear, 'respNumber': None if respNumber is None else min(respNumber, 100), 'circuitRef': f'%{circuitRef.lower()}%'}
		context = db.getRaceResults(params)
		
		data = dict()
		data['caption_text'] = 'result'
		data['titles'] = titles
		data['context'] = context
		
		return render_template('raceResults.html', context=data, circuitName=circuitRef, raceYear=raceYear, respNumber=len(context))
	else:
		return render_template('raceResults.html')
		
@app.route('/drivers', methods=['GET', 'POST'])
def drivers():
	context = db.getDrivers()
	
	data = {'context': context}
	return render_template('drivers.html', context=data)

@app.route('/drivers/<path:driverSlug>')
def driverDetails(driverSlug):
	return render_template('driver.html', driverInfo=driverSlug)

@app.route('/circuits', methods=['GET', 'POST'])
def circuits():
	context = db.getCircuits()
	data = {'context': context}
	return render_template('circuits.html', context=data)

@app.route('/circuits/<path:circuitName>')
def circuitDetails(circuitName):
	return render_template('circuit.html', circuitInfo=circuitName)

@app.route('/seasons', methods=['GET', 'POST'])
def seasons():
	raceYear = request.form.get('raceYear', default=None, type=str) or None
	context = db.getSeasons(raceYear)
	return render_template('seasons.html')

@app.route('/quiz', methods = ['GET', 'POST'])
def quiz():
	return render_template('quiz.html')
	
@app.route('/gameBlink', methods = ['GET', 'POST'])
def gameBlink():
	return render_template('gameBlink.html')

@app.route('/signUp', methods = ['GET', 'POST'])
def signUp():
	return render_template('signUp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username and password match a user in the database
        if db.getUsers(username) and db.getUsers() == password:
            return f'Welcome, {username}!'
        else:
            return 'Invalid username or password. Please try again.'

    # Render the login form for GET requests
    return render_template('login.html')

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
	return render_template('contact.html')

if __name__ == '__main__':
	app.run(host="127.0.0.1", port="5002", debug=True)
