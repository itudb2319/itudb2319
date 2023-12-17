from flask import request, render_template, Blueprint
from ..Modal.drivers import columnDict, getDrivers
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
	
@driversBP.route('/<path:driverSlug>')
def driverDetails(driverSlug):
	return render_template('driver.html', driverInfo=driverSlug)
