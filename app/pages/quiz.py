from flask import request, render_template, Blueprint, current_app

quizBP = Blueprint('quiz', __name__, url_prefix='/quiz')

@quizBP.route('/', methods = ['GET', 'POST'])
def quiz():
	return render_template('quiz.html')