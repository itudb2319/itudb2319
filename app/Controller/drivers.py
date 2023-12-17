from flask import request, render_template, Blueprint
from ..Modal.drivers import columnDict, getDrivers, getDriverCareer, getDriverPersonal
from app.Modal.filter import makeFilter
driversBP = Blueprint('drivers', __name__, url_prefix='/drivers')

@driversBP.route('/', methods=['GET', 'POST'])
def drivers():
	orderBy = "forename"
	search = ""
	if request.method == "POST":
		selectedColumns, context, orderBy = makeFilter(orderBy, getDrivers, request.form, list(columnDict.values()), "drivers", list(columnDict.keys()), **columnDict)

	elif request.method == "GET":
		context = getDrivers(list(columnDict.keys()), orderBy, search)
		selectedColumns = list(columnDict.values())

	data = {'columnDict': columnDict, 'headers': selectedColumns, 'context': context, 'orderBy': orderBy}	
	return render_template('drivers.html', context=data)
	
@driversBP.route('/<path:driverName>_<path:driverSurname>')
def driverDetails(driverName, driverSurname):
	params = {'sDriverName': driverName, 'sDriverSurname': driverSurname}

	careerInfo = getDriverCareer(params)
	personalInfo = getDriverPersonal(params)
	
	headerCareer = ['Race', 'Point', 'Wins', 'Podiums', 'DNFs']
	headerPersonal = ['Name', 'Surname', 'Seasons', 'Date Of Birth', 'Nationality', 'Number']

	data = {'personal': personalInfo, 'career': careerInfo, 'headerP': headerPersonal, 'headerC': headerCareer}
	return render_template('driver.html', context=data)

