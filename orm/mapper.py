from abc import ABCMeta, abstractmethod
from .database import Database
from datetime import datetime


class Mapper:
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert_to_db_value(self, cls, field_value):
        raise NotImplementedError

    @abstractmethod
    def find_objects_where(self, cls, where_clause):
        raise NotImplementedError

    @abstractmethod
    def delete_objects_where(self, cls, where_clause):
        raise NotImplementedError

    @abstractmethod
    def insert_object(self, cls, obj: object):
        raise NotImplementedError


class SQLiteMapper(Mapper):
    def __init__(self):
        pass

    @staticmethod
    def convert_to_db_value(field_value):
        '''Generate value for DB field from corresponding object field'''
        db_value = None
        if type(field_value) is int:
            db_value = int(field_value)
        elif type(field_value) is str:
            db_value = "'" + field_value + "'"
        elif type(field_value) is bool:
            db_value = int(field_value)
        elif type(field_value) is datetime:
            db_value = "'" + field_value.strftime("%d-%m-%Y") + "'"
        elif field_value is None:
            db_value = 'NULL'
        else:
            raise Exception('Unsupport type %s' % field_value)

        return db_value

    @staticmethod
    def find_objects_where(entity_cls, where_clause):
        column_list = ','.join(entity_cls.get_column_list())
        sql_str = 'SELECT ' + column_list + ' FROM ' + entity_cls.get_table_name() + ' WHERE ' + where_clause
        print(sql_str)
        db = Database.get_db_instance()
        cursor = db.cursor()
        results = []
        for db_row in cursor.execute(sql_str).fetchall():
            obj = entity_cls()
            obj.__dict__.update(dict(db_row))
            results.append(obj)

        return results

    @staticmethod
    def delete_objects_where(entity_cls, where_clause):
        sql_str = 'DELETE FROM ' + entity_cls.get_table_name() + ' WHERE ' + where_clause
        print(sql_str)
        db = Database.get_db_instance()
        cursor = db.cursor()
        cursor.execute(sql_str)
        db.commit()
        print('Delete successfully')

    @staticmethod
    def insert_object(entity_cls, obj_dict: dict):
        table_name = entity_cls.get_table_name()
        sql_fields_str = ''
        columns = entity_cls.get_column_list()
        column_fields = []
        for attr_name, attr_value in obj_dict.items():
            if attr_name in columns:
                db_field_value = SQLiteMapper.convert_to_db_value(attr_value)
                # Concat the fields' values
                if type(db_field_value) is int:
                    sql_fields_str += str(db_field_value)
                elif type(db_field_value) is str:
                    sql_fields_str += db_field_value

                sql_fields_str += ','

                column_fields.append(attr_name)

        if sql_fields_str[-1] == ',':
            sql_fields_str = sql_fields_str[:-1]

        if sql_fields_str:
            fields_to_insert = ','.join(column_fields)
            sql_str = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, fields_to_insert, sql_fields_str)
        else:
            raise Exception('Object attributes null')

        print(sql_str)
        db = Database.get_db_instance()
        cursor = db.cursor()
        cursor.execute(sql_str)
        db.commit()
        print('Insert successfully')
