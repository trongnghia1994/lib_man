from .base_table import BaseTable
from .database import Database


def execute_sql(sql_str):
    db = Database.get_db_instance()
    db.execute(sql_str)
