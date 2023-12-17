from flask import request, render_template, Blueprint
from ..Modal.drivers import columnDict, getDrivers
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
	
@driversBP.route('/<path:driverSlug>')
def driverDetails(driverSlug):
	return render_template('driver.html', driverInfo=driverSlug)
