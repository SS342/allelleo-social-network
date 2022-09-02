import sqlite3
import random
import uuid
import hashlib



class User(object):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        self.is_active = False  # must have this


class Passwords(object):
    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ":" + salt

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(":")
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    @staticmethod
    def generate_password(lenght: int = 20):
        password: str = ""
        for i in range(lenght):
            password += random.choice(list("-_--qweadszcvfrbgtnhymjukilopQASWEDFRTGHYUJKIOLPZXCVBNM1234567890"))
        return password

