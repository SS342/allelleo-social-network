import sqlite3
import os




class UsersDataBase(object):
    """Таблица в базе данных в которой будут храниться пользователи"""
    __tablename__ = 'users'

    def __init__(self, *, path=os.getcwd() + "\\static\\db\\main.db"):
        self.__connection__ = sqlite3.connect(path)
        self.__cursor__ = self.__connection__.cursor()
        self.__create_table()

    def __create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS `users` (
            id INT PRIMARY KEY NOT NULL,
            nickname VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL
        )
        """
        self.__cursor__.execute(sql)
        self.__connection__.commit()

    def get_user_by_id(self, user_id):
        sql = f"SELECT * FROM users WHERE id = {user_id}"
        result = self.__cursor__.execute(sql).fetchall()
        print(result)
        if result:
            res = result[0]
            return res
        else:
            return "ERR0R"
