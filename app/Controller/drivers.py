from flask import request, render_template, Blueprint, current_app
from ..Modal.drivers import getDrivers

driversBP = Blueprint('drivers', __name__, url_prefix='/drivers')

@driversBP.route('/', methods=['GET', 'POST'])
def drivers():

	if request.method == 'GET':
		context = getDrivers()
		data = {'context': context}
	return render_template('drivers.html', context=data)

@driversBP.route('/<path:driverSlug>')
def driverDetails(driverSlug):
	return render_template('driver.html', driverInfo=driverSlug)