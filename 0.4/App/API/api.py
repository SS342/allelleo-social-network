import flask

from DataBase.CheckToken import CheckToken
from DataBase.User.users import UsersDataBase

from DataBase.User.following_peoples import UserFollowingToUserDataBase

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


@api.route('/delete_following/<user_id>/<following_to>/<token>')
def delete_following(user_id, following_to, token):
    if CheckToken(user_id, token):
        UserFollowingToUserDataBase().delete_following(user_id, following_to)
        print("OK")
        return {'success': True}
    else:
        print("NOT OK")
        return {'error': "yes"}

@api.route('/new_following/<user_id>/<following_to>/<token>')
def new_following(user_id, following_to, token):
    if CheckToken(user_id, token):
        UserFollowingToUserDataBase().new_following(user_id, following_to)
    else:
        print("NOT OK")
        return {'error': "yes"}

