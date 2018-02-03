from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

class User:
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

class LoginForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()])
    submit = SubmitField('Log in')


login_manager = LoginManager()
login_manager.login_view = 'login'
bootstrap = Bootstrap()

admin = User('admin')
users = [admin]

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.get_id() == user_id:
            return user
    return None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'You will never guess'
    login_manager.init_app(app)
    bootstrap.init_app(app)
    return app


app = create_app()

@app.route('/')
def index():
    return 'Public index'

@app.route('/redirect')
def do_redirect():
    return redirect(url_for('index'))

@app.route('/restricted')
@login_required
def restricted():
    return "Restricted"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        for user in users:
            if user.username == username:
                login_user(user)
                return redirect(url_for('restricted'))
        return "Login failed"
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'