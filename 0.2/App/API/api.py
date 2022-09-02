import flask
from DataBase.users import UsersDataBase
api = flask.Blueprint('api', __name__)

@api.route('/status')
def status():
    return {'status': 'ok'}

@api.route('/unique_nickname/<nickname>')
def unique_nickname(nickname):
    if UsersDataBase().unique_nickname(nickname):
        return {'unique_nickname': 1}
    else:
        return {'unique_nickname': 0}




