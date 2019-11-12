import sqlite3


class Database:
    conn = None

    @staticmethod
    def init_db(conn_str):
        if Database.conn is None:
            Database.conn = sqlite3.connect(conn_str)
            Database.conn.row_factory = sqlite3.Row

    @staticmethod
    def get_db_instance():
        if Database.conn is None:
            raise Exception('No DB instance active now')
        else:
            return Database.conn

    @staticmethod
    def close():
        if Database.conn is not None:
            Database.conn.close()
        else:
            raise Exception('No DB instance active now')
