import os, sqlite3
from DataBase.User.users import UsersDataBase


class UserFollowingToUser(object):
    def __init__(self, user_id, Users: list):
        self.user_id = user_id
        self.Users = Users


class UserFollowingDisplay(object):
    def __init__(self, user_id, name, surname, nickname, avatar):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.avatar = avatar


class UserFollowingToUserDataBase(object):
    __tablename__ = 'user_following_to_user'

    def __init__(self, *, path=os.getcwd() + "\\dbs\\user_following_to_user.db"):
        self.__connection__ = sqlite3.connect(path)
        self.__cursor__ = self.__connection__.cursor()
        self.__create_table()

    def __create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS `user_following_to_user` (
            user_id INT NOT NULL,
            to_user INT NOT NULL
        );
        """
        self.__cursor__.execute(sql)
        self.__connection__.commit()

    def get_following(self, user_id):
        sql = f"SELECT to_user FROM `user_following_to_user` WHERE user_id = {user_id}"
        res = self.__cursor__.execute(sql).fetchall()
        if res:
            following = []
            for user in res:
                following.append(user[0])
            print(following)

            users = []
            for user in following:
                users.append(UsersDataBase().get_user_by_id(user))

            return UserFollowingToUser(user_id, users)

    def new_following(self, user_id, user_following_id):
        pass

    def delete_following(self, user_id, user_following_id):
        print(f"DELETE {user_id} ~ {user_following_id}")
        sql = f"DELETE FROM user_following_to_user WHERE user_id = {user_id} AND to_user = {user_following_id}"
        self.__cursor__.execute(sql)
        self.__connection__.commit()
