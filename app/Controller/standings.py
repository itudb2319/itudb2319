from flask import request, render_template, Blueprint
from ..Modal.getStandinds import getSeasonStandings

standingsBP = Blueprint('standings', __name__)

@standingsBP.route('/stand', methods=['GET', 'POST'])
def standing():
    if request.method == 'POST':
        data = dict()
        year = request.form.get('year', default=2022, type=int)
        data['titles'] = ['#', 'Name', 'Nationality', 'Points', 'Wins']
        data['context'] = getSeasonStandings(year)
        return render_template('standings.html', context=data)
    else:
        return render_template('standings.html')