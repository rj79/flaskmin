from flask import redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from app.main import bp
from app.main.forms import LoginForm
from app.model import users

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/redirect')
def do_redirect():
    return redirect(url_for('main.index'))

@bp.route('/restricted')
@login_required
def restricted():
    return render_template('restricted.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        for user in users:
            if user.username == username:
                login_user(user)
                return redirect(url_for('main.restricted'))
        return "Login failed"
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')
