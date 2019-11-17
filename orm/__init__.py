from .database import Database


def execute_sql(sql_str):
    db = Database.get_db_instance()
    cur = db.cursor()
    cur.execute(sql_str)
    db.commit()
