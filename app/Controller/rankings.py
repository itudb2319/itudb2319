from flask import request, render_template, Blueprint, current_app
from ..Modal.rankings import getRankings, getHeadersForRanking

rankingsBP = Blueprint('rankings', __name__, url_prefix='/rankings')
	
@rankingsBP.route('/', methods = ['GET', 'POST'])
def ratings():
	return render_template('rankings.html')

@rankingsBP.route('/<path:rankingName>')
def rankingDetails(rankingName):
	context = getRankings(rankingName)

	columns = getHeadersForRanking(rankingName)

	data = {'context': context, 'headers':columns}
	return render_template('rankingDetails.html', context=data)
