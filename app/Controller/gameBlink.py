from flask import request, render_template, Blueprint, session, redirect, url_for
from ..Modal.database import db

gameBlinkBP = Blueprint('gameBlink', __name__, url_prefix='/gameBlink')
	
@gameBlinkBP.route('/', methods = ['GET', 'POST'])
def gameBlink():
	if 'blinkscore' not in session.keys():
		return redirect(url_for('auth.login'))
	if request.method == 'POST':
		changedResult = session['blinkscore']
		if (session['blinkscore'] is not None):
			if (int(session['blinkscore']) > int(request.form.get('blinkResult'))):
				changedResult = int(request.form.get('blinkResult'))
		else:
			changedResult = int(request.form.get('blinkResult'))

		db.executeQuery(f'''
								UPDATE users SET blinkScore = {changedResult} WHERE userId = %s
								''', params=[session['userId']], commit=1)
		session['blinkscore'] = db.executeQuery('SELECT blinkScore FROM users WHERE userId = %s', params=[session['userId']], getData=1)
	return render_template('gameBlink.html')