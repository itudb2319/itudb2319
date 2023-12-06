from flask import request, render_template, Blueprint, redirect, url_for, g, flash, session
from ..Modal.authHelper import checkUser, registerUser
from werkzeug.security import generate_password_hash, check_password_hash
import functools

authBP = Blueprint('auth', __name__)

@authBP.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = checkUser(username, password)
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[5], password):
            error = 'Incorrect password.'
        else:
            session.clear()
            session['userId'] = user[0]
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

# decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view