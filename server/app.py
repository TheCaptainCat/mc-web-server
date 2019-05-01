from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO

from server import User

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


socketio = SocketIO(app)
