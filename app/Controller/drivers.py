from flask import request, render_template, Blueprint
from ..Modal.query import getTableQuery
from app.Controller.controllerShow import makeShow
driversBP = Blueprint('drivers', __name__, url_prefix='/drivers')

@driversBP.route('/', methods=['GET', 'POST'])
def drivers():
	columnDict = {
			"driverId": "ID",
			"forename": "Name",
			"surname": "Surname",
			"nationality": "Nationality",
			"number": "Number",
			"driverRef": "Reference", 
			"code": "Code",
			"dob": "Date of Birth"
			}
		
	defaultList = ["ID", "Name", "Surname", "Nationality", "Number"]
	defaultListKeys = ["driverId", "forename", "surname", "nationality", "number"]

	if request.method == "POST":
		selectedColumns, context = makeShow("driverId", request.form, defaultList, "drivers", defaultListKeys, **columnDict)

	elif request.method == "GET":
		context = getTableQuery("drivers", defaultListKeys)
		selectedColumns = defaultList
	
	del columnDict["driverId"]
	data = {'column_dict': columnDict, 'headers': selectedColumns, 'context': context}	
	return render_template('drivers.html', context=data)
	
@driversBP.route('/<path:driverSlug>')
def driverDetails(driverSlug):
	return render_template('driver.html', driverInfo=driverSlug)
