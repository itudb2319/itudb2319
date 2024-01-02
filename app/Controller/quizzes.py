from flask import request, render_template, Blueprint, session, redirect, url_for
from ..Modal.quizUtils import getQuestion, getCorrect
from ..Modal.database import db
from ..Controller.auth import loginRequired
import datetime, random

quizBP = Blueprint('quiz', __name__, url_prefix='/quiz')

@quizBP.route('/', methods = ['GET', 'POST'])
@loginRequired
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

		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		db.executeQuery(query=
			"""
				INSERT INTO answers(userid, quizid, time, istrue)
				VALUES(%s, %s, %s, %s)
			""",
			params=[int(session['userId']), int(quizId), now, isCorrect],
			commit=1
		)
		return render_template('quiz.html', show=False, isCorrect=isCorrect)
	
	result = getQuestion()
	if result is not None:
		quizId, content, option1, option2, correct = result
		options = [option1, option2, correct]
		random.shuffle(options)
		return render_template('quiz.html', show=True, quizId=quizId, question=content, options=options, empty=False)
	else:
		return render_template('quiz.html', show=True, empty=True)

@quizBP.route('/createQuiz', methods = ['GET', 'POST'])
@loginRequired
def createQuiz():
	if request.method == "GET":
		return render_template('cudQuiz.html', operation='create')
	else:
		question = request.form.get('content')
		falseAnswer1 = request.form.get('option1')
		falseAnswer2 = request.form.get('option2')
		correctAnswer = request.form.get('correct')

		db.executeQuery(
			"""
				INSERT INTO quiz(questioncontent, option1, option2, correctanswer)
				VALUES(%s, %s, %s, %s)
			""",
			params=[question, falseAnswer1, falseAnswer2, correctAnswer],
			commit=1
		)

		return redirect(url_for('quiz.quiz'))


@quizBP.route('/updateQuiz/<quiz_id>', methods = ['GET', 'POST'])
@loginRequired
def updateQuiz(quiz_id):
	if request.method == "GET":
		db.cur = db.conn.cursor()
		db.cur.execute("SELECT * FROM quiz WHERE quizid = %s", [int(quiz_id)])
		quiz = db.cur.fetchall()[0]
		return render_template('cudQuiz.html', operation='update', quiz=quiz)
	else:
		question = request.form.get('content')
		falseAnswer1 = request.form.get('option1')
		falseAnswer2 = request.form.get('option2')
		correctAnswer = request.form.get('correct')

		db.executeQuery(
			"""
				UPDATE quiz
				SET
					questioncontent = %s,
					option1 = %s,
					option2 = %s,
					correctanswer = %s
				WHERE quizid = %s
			""",
			params=[question, falseAnswer1, falseAnswer2, correctAnswer, int(quiz_id)],
			commit=1
		)

		return redirect(url_for('quiz.quiz'))
	
@quizBP.route('/deleteQuiz/<quiz_id>', methods = ['GET', 'POST'])
@loginRequired
def deleteQuiz(quiz_id):
	if request.method == "POST":
		db.executeQuery("DELETE FROM quiz WHERE quizid = %s", params=[int(quiz_id)], commit=1)
		return redirect(url_for('quiz.quiz'))
