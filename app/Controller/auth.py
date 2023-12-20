from flask import request, render_template, Blueprint, redirect, url_for, session, flash
from ..Modal.authHelper import getUser, registerUser, deleteUser, updateUser
from werkzeug.security import generate_password_hash, check_password_hash
import functools

# decorator
def isAdmin(view):
    @functools.wraps(view)
    def wrappedView(**kwargs):
        if session.get('role') is not None:
            if session['role'] == 1:
                pass
            else:
                return 'You are not authorized for admin role!'
        else:
            return 'You are not logged in!'
        return view(**kwargs)

    return wrappedView

# decorator
def loginRequired(view):
    @functools.wraps(view)
    def wrappedView(**kwargs):
        if session.get('userId') is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrappedView

authBP = Blueprint('auth', __name__)

@authBP.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = getUser(username)
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
            session['role'] = user[8] # 1 is for admin 0 is for user
            return redirect(url_for('index'))
            
    return render_template('login.html', error=error)

@authBP.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pswHash = generate_password_hash(password)
        error = registerUser(username, pswHash, role=0)
        if error is None:
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', error=error)

@authBP.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@authBP.route('/user', methods=['GET', 'POST'])
@loginRequired
def user():
    error = None
    if request.method == 'POST':
        # Delete user
        if request.form.get('userName') is None:
            error = deleteUser(session['userId'])
            if error is None:
                session.clear()
                return redirect(url_for('index'))
        # Update
        else:
            error = updateUser({
                'userName': request.form.get('userName'),
                'email': request.form.get('email'),
                'userId': session['userId']
                })
            
            if error is None:
                user = getUser(request.form.get('userName'))
                session['userId'] = user[0]
                session['userName'] = user[1]
                session['pp'] = user[2]
                session['blinkscore'] = user[3]
                session['email'] = user[4]
                session['quizscore'] = user[7]
                session['role'] = user[8] # 1 is for admin 0 is for user

        
    return render_template('user.html', error=error)
