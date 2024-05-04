import random

import psycopg2
from contextlib import contextmanager


class Db:
    database = None
    user = None
    password = None
    port = None
    host = None

    def __init__(self, database, user, password, port, host):
        try:
            self.database = database
            self.user = user
            self.password = password
            self.port = port
            self.host = host
            self.connection = None
        except ValueError:
            print("Database connection failed")

    @contextmanager
    def set_connect(self):
        try:
            self.connection = psycopg2.connect(database=self.database,
                                               user=self.user,
                                               password=self.password,
                                               port=self.port,
                                               host=self.host)
            self.connection.autocommit = True

            print(f"Successfully connected to the database: {self.database}")
            yield self.connection
            self.connection.rollback()
            self.connection.close()
            print(f"Successfully disconnected from the database: {self.database}")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.connection:
                self.connection.close()

    def query(self, query, data=None):
        with self.set_connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)

    def fetch_all(self, query, data=None) -> list:
        with self.set_connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)
            return cursor.fetchall()

    def fetch_one(self, query, data=None):
        with self.set_connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)
            result = cursor.fetchone()
            return result[0]

    def drop_table(self, table_name):
        self.query(f"DROP TABLE IF EXISTS {table_name};")

    def truncate_table(self, table_name):
        self.query(f"TRUNCATE TABLE {table_name};")
