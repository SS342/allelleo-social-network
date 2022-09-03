import sqlite3
import os
from datetime import date
from Configs.app_config import config

# from DataBase.User.users import UsersDataBase


get_date = lambda: str(date.today())
get_sex = lambda flag: str(config['DataBase']['User']['profile']['all_sex'].get(str(flag), 'Not stated'))
get_status = lambda flag: str(config['DataBase']['User']['profile']['all_status'].get(str(flag), 'Not stated')) if str(
    flag) != '0' else "Not stated"
get_location = lambda flag: flag if str(flag) != '0' else "Not stated"
get_work = lambda flag: flag if str(flag) != '0' else "Not stated"
get_birth_date = lambda flag: flag if str(flag) != '0' else "Not stated"


class UserProfile(object):
    def __init__(self, user_id, description, sex, birth_date, first_login, status, work, location, id):
        self.user_id = user_id
        self.description = description
        self.sex = sex
        self.birth_date = birth_date
        self.first_login = first_login
        self.status = status
        self.work = work
        self.location = location
        self.id = id

    def get_profile_id(self):
        return int(self.id)

    def get_user_id(self):
        return int(self.user_id)

    def update_profile(self, data):
        UserProfileDataBase().update_profile(self.user_id, data)


class UserProfileDataBase(object):
    __tablename__ = 'profiles'

    def __init__(self, *, path=os.getcwd() + "\\dbs\\profiles.db"):
        self.__connection__ = sqlite3.connect(path)
        self.__cursor__ = self.__connection__.cursor()
        self.__create_table()

    def __create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS `profiles` (
            user_id INT NOT NULL,
            description VARCHAR(500) NOT NULL,
            sex INT NOT NULL,
            birth_date VARCHAR(255) NOT NULL,
            first_login VARCHAR(255) NOT NULL,
            status INT NOT NULL DEFAULT 0,
            work VARCHAR(255) NOT NULL DEFAULT '0',
            location VARCHAR(255) NOT NULL DEFAULT '0',
            id INT PRIMARY KEY NOT NULL
        );
        """
        self.__cursor__.execute(sql)
        self.__connection__.commit()

    def get_user_profile_by_id(self, user_id):
        sql = f"SELECT * FROM `profiles` WHERE user_id={user_id}"
        res = self.__cursor__.execute(sql).fetchall()
        if res:
            return UserProfile(
                user_id=int(res[0][0]),
                description=res[0][1],
                sex=get_sex(res[0][2]),
                birth_date=get_birth_date(res[0][3]),
                first_login=res[0][4],
                status=get_status(res[0][5]),
                work=get_work(res[0][6]),
                location=get_location(res[0][7]),
                id=res[0][8]
            )
        else:
            return "Error"

    def new_profile(self, user_id):
        sql = f"INSERT INTO profiles (user_id, description, sex, birth_date, first_login, id) VALUES ('{user_id}', ' ', 0, '0', '{get_date()}', {UserProfileDataBase().get_last_id()}) "
        self.__cursor__.execute(sql)
        self.__connection__.commit()

    def get_last_id(self):
        sql = f"SELECT * FROM profiles"
        res = self.__cursor__.execute(sql).fetchall()
        print(res)
        if res:
            return int(res[-1][0]) + 1
        else:
            return 0

    def update_profile(self, data, user):
        if not (data['email'] == user.email):
            from DataBase.User.users import UsersDataBase
            UsersDataBase().user_update_email(user.id, data['email'])
        if not (data['name'] == user.name):
            from DataBase.User.users import UsersDataBase
            UsersDataBase().user_update_name(user.id, data['name'])
        if not (data['surname'] == user.surname):
            from DataBase.User.users import UsersDataBase
            UsersDataBase().user_update_surname(user.id, data['surname'])
        if not (data['nickname'] == user.nickname):
            from DataBase.User.users import UsersDataBase
            UsersDataBase().user_update_nickname(user.id, data['nickname'])

        birth_date = data['birth_date']
        about = data['about']
        sql = f"UPDATE profiles SET birth_date='{birth_date}', description='{about}' WHERE user_id={data['user_id']}"
        self.__cursor__.execute(sql)
        self.__connection__.commit()
