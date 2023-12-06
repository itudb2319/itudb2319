from flask import render_template
from app.Modal.raceResults import getLastRaceBestLaps
from app import create_app

app = create_app()

@app.route('/')
def index():
    data = dict()
    data['titles'] = ['Circuit', 'Lap', 'Time', 'Name', 'Nationality']
    data['context'] = getLastRaceBestLaps()
    return render_template('index.html', context=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)
