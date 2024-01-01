from app.Modal.database import db

def getQuestion():
    results = db.executeQuery('''
                              SELECT quizid, questionContent, option1, option2, correctAnswer
                              FROM quiz
                              ORDER BY random()
                              LIMIT 1;
                              ''')
    if len(results):
        return results[0]
    return None

def getCorrect(quizId):
    results = db.executeQuery('''
                              SELECT correctanswer
                              FROM quiz
                              WHERE quizid = %s
                              ''', params=[int(quizId)], getData=1)
    return results

