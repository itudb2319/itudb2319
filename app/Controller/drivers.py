from flask import request, render_template, Blueprint
from ..Model.drivers import getDriverCareer, getDriverPersonal
from ..Controller.genericController import GenericController
from ..Model.utilities import getColumns
from flask import Blueprint

tableName = "drivers"

from ..Model.utilities import getPrimary
id = getPrimary(tableName=tableName)[0][0]

driversBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

drivers = GenericController(tableName, allColumns, id, "drivers.html")
drivers.render(driversBP)
	
@driversBP.route('/<path:driverId>')
def driverDetails(driverId):
	params = {'sDriverId': driverId}

	careerInfo = getDriverCareer(params)
	personalInfo = getDriverPersonal(params)
	
	headerCareer = ['Season', 'Race', 'Point', 'Wins', 'Podiums', 'DNFs']
	headerPersonal = ['Name', 'Surname', 'Seasons', 'Date Of Birth', 'Nationality', 'Number']

	data = {'personal': personalInfo, 'career': careerInfo, 'headerP': headerPersonal, 'headerC': headerCareer}
	return render_template('driver.html', context=data)
