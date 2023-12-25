from app.Modal.database import db

def getQuestion():
    results = db.executeQuery('''
                              SELECT quizid, questionContent, option1, option2, correctAnswer
                              FROM quiz
                              ORDER BY random()
                              LIMIT 1;
                              ''')
    return results[0]

def getCorrect(quizId):
    results = db.executeQuery('''
                              SELECT correctAnswer
                              FROM quiz
                              WHERE %s
                              ''', params=[quizId], getData=1)
    return results
