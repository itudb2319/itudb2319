from flask import request, render_template, Blueprint, session
from ..Modal.quizUtils import getQuestion, getCorrect
from ..Modal.database import db

quizBP = Blueprint('quiz', __name__, url_prefix='/quiz')

@quizBP.route('/', methods = ['GET', 'POST'])
def quiz():
	if request.method == 'POST':
		quizId = request.form.get('quizid')
		correctAnswer = request.form.get('answer')
		isCorrect = getCorrect(quizId) == correctAnswer
		if isCorrect:
			db.executeQuery('''
							UPDATE users SET quizScore = COALESCE((SELECT quizScore FROM users WHERE userId = %s), 0) + 1 WHERE userId = %s
							''', params=[session['userId'], session['userId']], commit=1)
			session['quizscore'] = db.executeQuery('SELECT quizScore FROM users WHERE userId = %s', params=[session['userId']], getData=1)
		return render_template('quiz.html', show=False, isCorrect=isCorrect)
	
	quizId, content, option1, option2, correct = getQuestion()
	
	return render_template('quiz.html', show=True, quizId=quizId, question=content, correct=correct, falseAnswers=[option1, option2])