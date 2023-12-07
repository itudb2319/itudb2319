from flask import request, render_template, Blueprint, current_app
from ..Modal.circuits import columnDict, defaultList, defaultListKeys, getCircuits
from app.Controller.controllerFilter import makeFilter
circuitsBP = Blueprint('circuits', __name__, url_prefix='/circuits')

@circuitsBP.route('/', methods=['GET', 'POST'])
def circuits():
	if request.method == "POST":
		selectedColumns, context, orderBy = makeFilter("circuitId", getCircuits, request.form, defaultList, "circuits", defaultListKeys, **columnDict)

	elif request.method == "GET":
		context = getCircuits(defaultListKeys)
		selectedColumns = defaultList
		orderBy = "circuitId"
	
	data = {'columnDict': columnDict, 'headers': selectedColumns, 'context': context, 'orderBy': orderBy}	
	return render_template('circuits.html', context=data)

@circuitsBP.route('/<path:circuitName>')
def circuitDetails(circuitName):
	return render_template('circuit.html', circuitInfo=circuitName)