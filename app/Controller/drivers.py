from flask import request, render_template, Blueprint
from ..Modal.drivers import columnDict, getDrivers, getDriverCareer, getDriverPersonal
from app.Modal.filter import makeFilter
import math
driversBP = Blueprint('drivers', __name__, url_prefix='/drivers')

@driversBP.route('/', methods=['GET', 'POST'])
def drivers():
	orderBy = "forename"
	search = ""
	page = "1"
	if request.method == "POST":
		selectedColumns, context, orderBy, length, page = makeFilter(orderBy, getDrivers, request.form, list(columnDict.values()), "drivers", list(columnDict.keys()), page, **columnDict)

	elif request.method == "GET":
		context, length = getDrivers(list(columnDict.keys()), orderBy, search, page)
		selectedColumns = list(columnDict.values())

	data = {'columnDict': columnDict, 'headers': selectedColumns, 'context': context, 'orderBy': orderBy, 'length': math.ceil(length / 20), 'currentPageNumber': page, 'lastSearched': search}	
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
