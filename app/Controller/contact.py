from flask import request, render_template, Blueprint, current_app

contactBP = Blueprint('contact', __name__, url_prefix='/contact')

@contactBP.route('/', methods = ['GET', 'POST'])
def contact():
	return render_template('contact.html')