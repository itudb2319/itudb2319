from flask import request, render_template, Blueprint, current_app
from ..Modal.query import getTableQuery
from app.Controller.controllerShow import makeShow
circuitsBP = Blueprint('circuits', __name__, url_prefix='/circuits')

@circuitsBP.route('/', methods=['GET', 'POST'])

def circuits():
	column_dict = {"circuitId": "ID",
			"name": "Name",
			"location": "Location",
			"country": "Country",
			"circuitRef": "Reference", 
			"lat": "Latitude",
			"lng": "Longitude",
			"alt": "Altitude"
			}
	
	default_list = ["ID", "Name", "Location", "Country", "Reference"]
	default_list_keys = ["circuitId", "name", "location", "country", "circuitRef"]

	if request.method == "POST":
		selected_columns, context = makeShow("circuitId", request.form, default_list, "circuits", default_list_keys, **column_dict)

	elif request.method == "GET":
		context = getTableQuery("circuits", default_list_keys)
		selected_columns = default_list
	
	del column_dict["circuitId"]
	data = {'column_dict': column_dict, 'headers': selected_columns, 'context': context}	
	return render_template('circuits.html', context=data)


@circuitsBP.route('/<path:circuitName>')
def circuitDetails(circuitName):
	return render_template('circuit.html', circuitInfo=circuitName)