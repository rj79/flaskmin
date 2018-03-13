from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from app.model import users

login_manager = LoginManager()
login_manager.login_view = 'main.login'
bootstrap = Bootstrap()

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

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
