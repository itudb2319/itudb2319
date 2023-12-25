from flask import request, render_template, Blueprint, current_app
from ..Modal.rankings import getRankings, getHeadersForRanking

rankingsBP = Blueprint('rankings', __name__, url_prefix='/rankings')
	
@rankingsBP.route('/', methods = ['GET', 'POST'])
def rankings():
	return render_template('rankings.html')

@rankingsBP.route('/<path:rankingName>', methods = ['GET', 'POST'])
def rankingDetails(rankingName):
	if request.method == 'POST':
		limNumber = request.form.get('limNumber', default=None, type=int)
		params = {'slimNumber' : limNumber}
		
		context = getRankings(rankingName, params)
		columns = getHeadersForRanking(rankingName)
		data = {'context': context, 'headers':columns, 'HEADER': rankingName}
		return render_template('rankingDetails.html', context=data, limNumber=len(context))
	else:
		limNumber = 5
		params = {'slimNumber' : limNumber}
		
		context = getRankings(rankingName, params)
		columns = getHeadersForRanking(rankingName)
		data = {'context': context, 'headers':columns, 'HEADER': rankingName}
		return render_template('rankingDetails.html', context=data, limNumber=len(context))
