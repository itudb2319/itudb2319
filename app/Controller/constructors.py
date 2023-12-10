from flask import request, render_template, Blueprint, current_app
from ..Modal.constructors import getConstructors

constructorsBP = Blueprint('constructors', __name__, url_prefix='/constructors')

@constructorsBP.route('/', methods=['GET', 'POST'])
def constructors():
	context = getConstructors()
	data = {'context': context}
	return render_template('constructors.html', context=data)