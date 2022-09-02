import datetime
import sqlite3
import os
from DataBase.User.profile import UserProfileDataBase


class User(object):
    """Создает объкт пользователя с его данными чтобы можно было легко их юзать в шаблонах и др"""

    def __init__(self, id, nickname, name, surname, email, hashed_password,
                 followers, following, avatar, posts):
        self.id = id
        self.nickname = nickname
        self.name = name
        self.surname = surname
        self.email = email
        self.hashed_password = hashed_password
        self.followers = followers
        self.following = following
        self.is_authenticated = True  # must have this
        self.is_active = True  # must have this
        self.avatar = avatar
        self.posts = posts

    def get_id(self):
        return int(self.id)

    @property
    def get_profile_data(self):
        return UserProfileDataBase().get_user_profile_by_id(self.id)

    def update_profile(self, data):
        UserProfileDataBase().update_user_profile(data)

class AnonymousUser(object):
    def __init__(self):
        self.login_time = datetime.datetime.now()
        self.is_authenticated = False
        self.is_active = True  # must have this


class UsersDataBase(object):
    """Таблица в базе данных в которой будут храниться пользователи"""
    __tablename__ = 'users'

    def __init__(self, *, path=os.getcwd() + "\\dbs\\auth.db"):
        self.__connection__ = sqlite3.connect(path)
        self.__cursor__ = self.__connection__.cursor()
        self.__create_table()

    def __create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS `users` (
            id INT PRIMARY KEY NOT NULL,
            nickname VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            hashed_passwords VARCHAR(255) NOT NULL,
            posts INT NOT NULL DEFAULT 0,
            followers INT NOT NULL DEFAULT 0,
            following INT NOT NULL DEFAULT 0,
            avatar VARCHAR(255) NOT NULL DEFAULT '../../static/img/default/defaultAvatar.jpg',
            bg_avatar VARCHAR(255) NOT NULL DEFAULT '../../static/img/default/defaultBgAvatar.jpg',
            token VARCHAR(255) NOT NULL
        );
        """
        self.__cursor__.execute(sql)
        self.__connection__.commit()

    def get_user_by_id(self, user_id):
        sql = f"SELECT * FROM users WHERE id = {user_id}"
        result = self.__cursor__.execute(sql).fetchall()

        if result:
            res = result[0]

            data = {
                'id': res[0],
                'nickname': res[1],
                'email': res[2],
                'name': res[3],
                'surname': res[4],
                'hashed_password': res[5],
                'posts': res[6],
                'followers': res[7],
                'following': res[8],
                'avatar': res[9]
            }

            # print(data)
            return User(id=data['id'], nickname=data['nickname'], email=data['email'], name=data['name'],
                        surname=data['surname'],
                        hashed_password=data['hashed_password'], posts=data['posts'],
                        followers=data['followers'], following=data['following'], avatar=data['avatar'])
        else:
            return 0

    def get_user_by_email(self, user_email):
        sql = f"SELECT * FROM users WHERE email='{user_email}'"
        result = self.__cursor__.execute(sql).fetchall()
        if result:
            res = result[0]
            data = {
                'id': res[0],
                'nickname': res[1],
                'email': res[2],
                'name': res[3],
                'surname': res[4],
                'hashed_password': res[5],
                'posts': res[8],
                'followers': res[9],
                'following': res[10],
                'avatar': res[11]
            }
            return User(id=data['id'], nickname=data['nickname'], email=data['email'], name=data['name'],
                        surname=data['surname'],
                        hashed_password=data['hashed_password'], posts=data['posts'],
                        followers=data['followers'], following=data['following'], avatar=data['avatar'])
        else:
            return 0

    def unique_nickname(self, user_nickname):
        sql = f"SELECT * FROM users WHERE nickname='{user_nickname}'"
        result = self.__cursor__.execute(sql).fetchall()
        if result:
            return False
        return True

    def new_user(self, nickname, email, name, surname, password, token):
        id = UsersDataBase().get_last_id()
        sql = f"INSERT INTO users (id, nickname, email, name, surname, hashed_passwords, token) VALUES ('{id}', '{nickname}', '{email}', '{name}', '{surname}', '{password}', '{token}') "
        UserProfileDataBase().new_profile(id)
        self.__cursor__.execute(sql)
        self.__connection__.commit()

    def get_last_id(self):
        sql = f"SELECT * FROM users"
        res = self.__cursor__.execute(sql).fetchall()
        print(res)
        if res:
            return int(res[-1][0]) + 1
        else:
            return 0

