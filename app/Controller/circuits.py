from flask import request, render_template, Blueprint, current_app
from ..Modal.circuits import getCircuits

circuitsBP = Blueprint('circuits', __name__, url_prefix='/circuits')

@circuitsBP.route('/', methods=['GET', 'POST'])
def circuits():
	context = getCircuits()
	data = {'context': context}
	return render_template('circuits.html', context=data)

@circuitsBP.route('/<path:circuitName>')
def circuitDetails(circuitName):
	return render_template('circuit.html', circuitInfo=circuitName)