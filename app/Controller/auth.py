from flask import request, render_template, Blueprint, redirect, url_for, g, session
from ..Modal.authHelper import getUser, registerUser
from werkzeug.security import generate_password_hash, check_password_hash
import functools

authBP = Blueprint('auth', __name__)

@authBP.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = getUser(username, password)
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[5], password):
            error = 'Incorrect password.'
        else:
            session.clear()
            session['userId'] = user[0]
            session['userName'] = user[1]
            session['pp'] = user[2]
            session['blinkscore'] = user[3]
            session['email'] = user[4]
            session['quizscore'] = user[7]
            return redirect(url_for('index'))
            
    return render_template('login.html', error=error)

@authBP.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pswHash = generate_password_hash(password)
        error = registerUser(username, pswHash)
        if error is None:
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', error=error)

@authBP.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@authBP.route('/user')
def user():
    return str(dict(session.items()))

# decorator
def loginRequired(view):
    @functools.wraps(view)
    def wrappedView(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrappedView