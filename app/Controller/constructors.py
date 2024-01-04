from flask import request, render_template, Blueprint, flash
from ..Model.constructors import getConstructors, getConstructorDriver, getConstructorCircuit
from datetime import datetime
from flask import request, render_template, Blueprint
from ..Controller.genericController import GenericController
from ..Model.utilities import getColumns
from flask import Blueprint

id = "constructorid"
tableName = "constructors"

constructorsBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

constructors = GenericController(tableName, allColumns, id, "constructors.html")
constructors.render(constructorsBP)

@constructorsBP.route('/<path:constructorId>', methods=['GET', 'POST'])
def constructorDetails(constructorId):
	

	params = {'sConstructorId': constructorId, 'sYear' : None}
	headersDriver = ["Name", "Surname", "Constructor"]
	headersCircuit = ["Circuit", "Round", "Total Points", "Constructor"]

	data = {'user_input_year' : datetime.now().year}

	if request.method == 'POST':
		user_input_year = request.form.get('year')
		if user_input_year.isdigit():
			params['sYear'] = int(user_input_year) 
			data['user_input_year'] = int(user_input_year)
		else:
			flash('Invalid input. Please enter a valid year.')

	contextDriver = getConstructorDriver(params)
	contextCircuit = getConstructorCircuit(params)
	data.update({'contextDriver': contextDriver, 'contextCircuit' :contextCircuit,  'constructorId': constructorId, 'headersDriver': headersDriver, 'headersCircuit': headersCircuit})

	return render_template('constructor.html', context=data)
