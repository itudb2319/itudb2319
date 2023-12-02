from flask import request, render_template, Blueprint, current_app

seasonsBP = Blueprint('seasons', __name__, url_prefix='/seasons')

@seasonsBP.route('/', methods=['GET', 'POST'])
def seasons():
	titles=["Name", "Year"]
	if request.method == 'POST':
		year = request.form.get('year', default=None, type=str) or None
		
		params = {'sYear': year}
		context = current_app.db.getSeasons(params)
		
		data = dict()
		data['titles'] = titles
		data['context'] = context

		return render_template('seasons.html', context=data, year=year, respNumber=len(context))

	return render_template('seasons.html')
