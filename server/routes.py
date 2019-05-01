from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required

from server import app, User, ServerRunner


@app.route('/', methods=['GET'])
@login_required
def home_page():
    return render_template('home.html')


@app.route('/status')
def server_status():
    return ServerRunner.server_status()


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    login_user(User.get(1))
    return redirect(url_for('home_page'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))
