from flask import request, render_template, Blueprint, current_app

authBP = Blueprint('auth', __name__, url_prefix='/auth')

@authBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username and password match a user in the database
        if current_app.db.login(username, password):
            return f'Welcome, {username}!'
        else:
            return 'Invalid username or password. Please try again.'

    # Render the login form for GET requests
    return render_template('login.html')

@authBP.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        username = request.form.get('New Username')
        password = request.form.get('New Password')

        if current_app.db.userCheck(username, password):
            return 'ERROR! TRY AGAIN'
        else:
            current_app.db.signUp(username, password)
            return 'Account created successfully. You can now log in.'
    
    return render_template('signUp.html')

