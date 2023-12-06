from flask import request, render_template, Blueprint, current_app

gameBlinkBP = Blueprint('gameBlink', __name__, url_prefix='/gameBlink')
	
@gameBlinkBP.route('/', methods = ['GET', 'POST'])
def gameBlink():
	return render_template('gameBlink.html')