from flask import request, render_template, Blueprint
from ..Modal.drivers import getDrivers, getFilteredDrivers

driversBP = Blueprint('drivers', __name__, url_prefix='/drivers')

@driversBP.route('/', methods=['GET', 'POST'])
def drivers():
	selected_list = []
	selected_columns = []
	column_dict = {	"forename": "Name",
			"surname": "Surname",
			"nationality": "Nationality",
			"number": "Number",
			"driverRef": "Reference", 
			"code": "Code",
			"dob": "Date of Birth"
			}
	if request.method == "POST":
		for key, value in request.form.items():
			if value == 'on':
				selected_list.append(key)
				selected_columns.append(column_dict[key])
				
		if len(selected_list) != 0:
			print(selected_columns)
			context = getFilteredDrivers(selected_list)	
		
		else:
			context = getDrivers()
			selected_columns = ["Name", "Surname", "Nationality", "Number"]
				
	elif request.method == "GET":
		context = getDrivers()
		selected_columns = ["Name", "Surname", "Nationality", "Number"]

	data = {'column_dict': column_dict, 'headers': selected_columns, 'context': context}	
	return render_template('drivers.html', context=data)
	
@driversBP.route('/<path:driverSlug>')
def driverDetails(driverSlug):
	return render_template('driver.html', driverInfo=driverSlug)
