import os
import sqlite3


def CheckToken(user_id, token):
    connection = sqlite3.connect(os.getcwd() + "\\dbs\\auth.db")
    cursor = connection.cursor()
    sql = f"SELECT token FROM users WHERE id={user_id}"
    if token in cursor.execute(sql).fetchall()[0]:
        return True
    return False
