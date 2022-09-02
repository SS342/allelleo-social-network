import sqlite3
import os




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
            small_description VARCHAR(50) NOT NULL DEFAULT 'Hi!',
            big_description VARCHAR(255) NOT NULL DEFAULT 'Hello, Im using allelleo SN!',
            posts INT NOT NULL DEFAULT 0,
            followers INT NOT NULL DEFAULT 0,
            following INT NOT NULL DEFAULT 0,
            avatar VARCHAR(255) NOT NULL DEFAULT '../../static/img/default/defaultAvatar.jpg',
            bg-avatar VARCHAR(255) NOT NULL DEFAULT '../../static/img/default/defaultBgAvatar.jpg',
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
            return res
        else:
            return 0

    def get_user_by_email(self, user_email):
        sql = f"SELECT * FROM users WHERE email='{user_email}'"
        result = self.__cursor__.execute(sql).fetchall()
        if result:
            res = result[0]
            return res
        else:
            return 0

    def unique_nickname(self, user_nickname):
        sql = f"SELECT * FROM users WHERE nickname='{user_nickname}'"
        result = self.__cursor__.execute(sql).fetchall()
        if result:
            return False
        return True

    def new_user(self, nickname, email, name, surname, password):

        sql = f"INSERT INTO users (id, nickname, email, name, surname, hashed_passwords) VALUES ('{UsersDataBase().get_last_id()}', '{nickname}', '{email}', '{name}', '{surname}', '{password}') "
        print(sql)
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

# print(UsersDataBase().get_last_id())
