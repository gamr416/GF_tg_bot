import sqlite3


class DB:
    def __init__(self):
        pass

    def insert_noob(self, data):
        con = sqlite3.connect('db/database')
        cursor = con.cursor()
        print(data)
        command = cursor.execute(
            f"""INSERT INTO Users(FIO, age, password) VALUES('{data[0]}', {data[1]}, '{data[2]}')"""
        ).fetchall()
        con.commit()
        cursor.close()
        con.close()

    def delete(self):
        pass

    def sign_in(self, data):
        con = sqlite3.connect('db/database')
        cursor = con.cursor()
        command = cursor.execute(
            f"""SELECT id FROM Users WHERE FIO = '{''.join(data[0])}' AND password = '{''.join(data[1])}'"""
        ).fetchall()
        cursor.close()
        con.close()
        return command[0][0]

    def get_all_users(self):
        con = sqlite3.connect('db/database')
        cursor = con.cursor()
        command = cursor.execute(
            f"""SELECT * FROM Users """
        ).fetchall()
        cursor.close()
        con.close()
        return command[0]
