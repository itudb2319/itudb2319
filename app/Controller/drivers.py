from flask import request, render_template, Blueprint
from ..Modal.drivers import columnDict, defaultList, defaultListKeys, getDrivers
from app.Controller.controllerFilter import makeFilter
driversBP = Blueprint('drivers', __name__, url_prefix='/drivers')

@driversBP.route('/', methods=['GET', 'POST'])
def drivers():
	if request.method == "POST":
		selectedColumns, context, orderBy = makeFilter("driverId", getDrivers, request.form, defaultList, "drivers", defaultListKeys, **columnDict)

	elif request.method == "GET":
		context = getDrivers(defaultListKeys)
		selectedColumns = defaultList
		orderBy = "driverId"
	
	data = {'columnDict': columnDict, 'headers': selectedColumns, 'context': context, 'orderBy': orderBy}	
	return render_template('drivers.html', context=data)
	
@driversBP.route('/<path:driverSlug>')
def driverDetails(driverSlug):
	return render_template('driver.html', driverInfo=driverSlug)
