import sqlite3


class Database:
    conn = None

    @staticmethod
    def init_db(conn_str, dbms='sqlite'):
        if Database.conn is None:
            if dbms == 'sqlite':
                Database.conn = sqlite3.connect(conn_str, check_same_thread=False)
                Database.conn.row_factory = sqlite3.Row
            else:
                raise Exception('DBMS %s not support' % dbms)

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
