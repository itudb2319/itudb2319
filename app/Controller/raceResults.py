from flask import request, render_template, Blueprint, current_app
from ..Modal.raceResults import getRaceResults

raceResultsBP = Blueprint('raceResults', __name__, url_prefix='/raceResults')

@raceResultsBP.route('/', methods=['GET', 'POST'])
def raceResults():
	titles=["Name", "Surname", "Nationality", "No.", "Circuit name", "Year", "fastest lap", "position", "position text*"]
	
	if request.method == 'POST':
		raceYear = request.form.get('raceYear', default=None, type=str) or None
		respNumber = request.form.get('respNumber', default=None, type=int)
		circuitRef = request.form.get('circuitRef', default='', type=str).lower()
		
		params = {'raceYear': raceYear, 'respNumber': None if respNumber is None else min(respNumber, 100), 'circuitRef': f'%{circuitRef.lower()}%'}
		context = getRaceResults(params)
		
		data = dict()
		data['caption_text'] = 'result'
		data['titles'] = titles
		data['context'] = context
		
		return render_template('raceResults.html', context=data, circuitName=circuitRef, raceYear=raceYear, respNumber=len(context))
	else:
		return render_template('raceResults.html')
