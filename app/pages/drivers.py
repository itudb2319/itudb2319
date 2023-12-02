from flask import request, render_template, Blueprint, current_app

driversBP = Blueprint('drivers', __name__, url_prefix='/drivers')

@driversBP.route('/', methods=['GET', 'POST'])
def drivers():
	context = current_app.db.getDrivers()
	
	data = {'context': context}
	return render_template('drivers.html', context=data)

@driversBP.route('/<path:driverSlug>')
def driverDetails(driverSlug):
	


	return render_template('driver.html', driverInfo=driverSlug)