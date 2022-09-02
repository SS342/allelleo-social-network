import flask
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
import random
import sqlite3
from Logs.logs import Logs
from DataBases.users import UsersDataBase

app = flask.Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'
app.config['SECRET_KEY'] = "IESBaofWPIfhohw398fheIUFEWGF(W3fsdbOU#F(WFGEJDSBIUW#"
app.config['JSON_AS_ASCII'] = False
app.config['APPLICATION_ROOT'] = '/'
app.config['MAX_COOKIE_SIZE'] = 8 * 1024


class User(object):
    """Создает объкт пользователя с его данными чтобы можно было легко их юзать в шаблонах и др"""

    def __init__(self, id, nickname, name, surname):
        self.id = id
        self.nickname = nickname
        self.name = name
        self.surname = surname
        self.is_active = True  # must have this

    def get_id(self):
        return str(self.id)


# INSERT INTO users (name, password) VALUES ('allelleo2', 'allelleo2')

UsersDataBase()
Logs()


@login_manager.user_loader
def load_user(user_id):
    data = UsersDataBase().get_user_by_id(user_id)
    user = User(data[0], data[1], data[2], data[3])
    return user


@app.route('/login', methods=['POST', 'GET'])
def LoginUser():
    if flask.request.method == 'POST':
        nick = flask.request.form['nick']
        password = flask.request.form['password']
        data = UsersDataBase().get_user_by_id(int(nick))

        user = User(data[0], data[1], data[2], data[3])
        print(f"USER LOGIN: {user.nickname}")
        if user:
            # if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            print(user)
            return str(current_user.name)
            # else:
            # return "В ДОСТУПЕ ОТКАЗАННО"
        else:
            return "В ДОСТУПЕ ОТКАЗАННО"

    return flask.render_template('auth/login.html')


app.run(debug=True)
