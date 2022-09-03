import flask
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
import random
import sqlite3

from DataBase.User.profile import UserProfileDataBase
from Logs.logs import Logs
from DataBase.User.users import UsersDataBase, User, update_profile
from Defense.passwords import Passwords
from Defense.token import generate_token
from API.api import api

UserProfileDataBase()

app = flask.Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in'
app.config['SECRET_KEY'] = "IESBaofWPIfhohw398fheIUFEWGF(W3fsdbOU#F(WFGEJDSBIUW#"
app.config['JSON_AS_ASCII'] = False
app.config['APPLICATION_ROOT'] = '/'
app.config['MAX_COOKIE_SIZE'] = 8 * 1024

app.register_blueprint(api, url_prefix="/api/v1")

# INSERT INTO users (id, nickname, email, name, surname, hashed_passwords) VALUES (0, 'allelleo', 'alex2005ov@gmail.com', 'Alexey', 'Ovchinnikov', 'fc300febae3b9a55723b7aecab31ce4469af3ad26501a982e416c6ac3471bb06:5fee1bad50e54831b1b3d9ee3c814962')

UsersDataBase()
Logs()


@login_manager.user_loader
def load_user(user_id):
    user = UsersDataBase().get_user_by_id(user_id)
    if user:

        return user
    return None


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return flask.redirect('/auth/sign-in')


@app.route('/auth/sign-in', methods=['POST', 'GET'])
def sign_in():
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = flask.request.form['password']
        print(f"USER LOGIN: {email} ~ {password}")
        user = UsersDataBase().get_user_by_email(email)
        if user:
            if Passwords().check_password(user.hashed_password, password):
                login_user(user)
                print(user)
                return flask.redirect(flask.url_for('home'))
    return flask.render_template('auth/sign-in.html')


@app.route('/auth/sign-up', methods=['POST', "GET"])
def sign_up():
    if flask.request.method == 'POST':
        # TODO: sql-injection checker;
        UsersDataBase().new_user(flask.request.form['nickname'], flask.request.form['email'],
                                 flask.request.form['name'], flask.request.form['surname'],
                                 Passwords().hash_password(flask.request.form['password']), token=generate_token())
        return flask.redirect('/auth/sign-in')
    return flask.render_template('auth/sign-up.html')


@app.route('/home')
@login_required
def home():
    # print(current_user.avatar)
    return flask.render_template('main_pages/home.html', user=current_user)


@app.route('/my-profile')
@login_required
def my_profile():
    return flask.render_template('user/my-profile.html', user=current_user)


@app.route('/my-profile/edit', methods=['POST', 'GET'])
@login_required
def my_profile_edit():
    if flask.request.method == 'POST':
        data = {
            'user_id': current_user.id,
            'name': flask.request.form['name1'],
            'surname': flask.request.form['surname'],
            'nickname': flask.request.form['nickname'],
            'birth_date': flask.request.form['birth_date'],
            'email': flask.request.form['email'],
            'about': flask.request.form['about']
        }

        print(data)
        update_profile(data, current_user)

    return flask.render_template('user/settings.html', user=current_user)

server = 'localhost'
port = 5000

app.run(debug=True)
