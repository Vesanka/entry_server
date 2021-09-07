import json
import sqlite3
import os


class SqliteManager():

    def __init__(self, db_name):

        path = 'server/db/'
        isExist = os.path.exists(path)

        if not isExist:
            os.mkdir(path)

        self.db = sqlite3.connect(f'{path}{db_name}')
        self.coursor = self.db.cursor()

    def close(self):
        self.db.close()

    def do_create(self, table_name, **kwargs):

        sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
        """
        for arg_name, arg_value in kwargs.items():
            sql += f'{arg_name} {arg_value}, '

        sql = sql[:-2] + ')'
        self.coursor.execute(sql)
        self.db.commit()

    def do_select_all(self, table_name):

        sql = f"""SELECT * FROM {table_name}"""

        return self.coursor.execute(sql).fetchall()

    def do_insert(self, table_name, json_data):

        sql = f"""INSERT INTO {table_name} ("""

        for key, _ in json.loads(json_data).items():
            sql += f'{key}, '
        sql = sql[:-2] + ') VALUES('

        for _, value in json.loads(json_data).items():
            sql += f'{value}, '

        sql = sql[:-2] + ');'

        self.coursor.execute(sql)
        self.db.commit()
