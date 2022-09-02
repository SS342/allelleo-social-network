import flask
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
import random
import sqlite3
from Logs.logs import Logs
from DataBase.users import UsersDataBase, User
from Defense.passwords import Passwords
from API.api import api

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
    data = UsersDataBase().get_user_by_id(user_id)
    if data:
        user = User(id=data[0], nickname=data[1], email=data[2], name=data[3], surname=data[4], hashed_password=data[5],
                    small_description=data[6], big_description=data[7], posts=data[8], followers=data[9],
                    following=data[10], avatar=data[11])
        return user
    return None


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return flask.redirect('/sign-in')


@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = flask.request.form['password']
        print(f"USER LOGIN: {email} ~ {password}")
        user = UsersDataBase().get_user_by_email(email)
        if user:
            user = User(id=user[0], nickname=user[1], email=user[2], name=user[3], surname=user[4],
                        hashed_password=user[5], small_description=user[6], big_description=user[7], posts=user[8],
                        followers=user[9], following=user[10], avatar=user[11])
            if Passwords().check_password(user.hashed_password, password):
                login_user(user)
                print(user)
                return flask.redirect(flask.url_for('home'))
    return flask.render_template('auth/sign-in.html')


@app.route('/sign-up', methods=['POST', "GET"])
def sign_up():
    if flask.request.method == 'POST':
        nickname = flask.request.form['nickname']
        email = flask.request.form['email']
        name = flask.request.form['name']
        surname = flask.request.form['surname']
        password = flask.request.form['password']
        # TODO: sql-injection checker;
        UsersDataBase().new_user(nickname, email, name, surname, Passwords().hash_password(password))
        return flask.redirect('/sign-in')
    return flask.render_template('auth/sign-up.html')


@app.route('/my-page')
@login_required
def home():
    print(current_user.nickname)
    return flask.render_template('main_pages/index.html', user=current_user)


app.run(debug=True)
