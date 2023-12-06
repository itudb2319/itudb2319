from flask import request, render_template, Blueprint
from ..Modal.query import getTableQuery
from app.Controller.controllerShow import makeShow
driversBP = Blueprint('drivers', __name__, url_prefix='/drivers')

@driversBP.route('/', methods=['GET', 'POST'])
def drivers():
	column_dict = {
			"driverId": "ID",
			"forename": "Name",
			"surname": "Surname",
			"nationality": "Nationality",
			"number": "Number",
			"driverRef": "Reference", 
			"code": "Code",
			"dob": "Date of Birth"
			}
		
	default_list = ["ID", "Name", "Surname", "Nationality", "Number"]
	default_list_keys = ["driverId", "forename", "surname", "nationality", "number"]

	if request.method == "POST":
		selected_columns, context = makeShow("driverId", request.form, default_list, "drivers", default_list_keys, **column_dict)

	elif request.method == "GET":
		context = getTableQuery("drivers", default_list_keys)
		selected_columns = default_list
	
	del column_dict["driverId"]
	data = {'column_dict': column_dict, 'headers': selected_columns, 'context': context}	
	return render_template('drivers.html', context=data)
	
@driversBP.route('/<path:driverSlug>')
def driverDetails(driverSlug):
	return render_template('driver.html', driverInfo=driverSlug)
