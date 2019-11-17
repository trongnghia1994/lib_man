from .database import Database
from .fields import BaseField, IntegerField, TextField, BooleanField, DateField
from .mapper import SQLiteMapper
from .query import QueryObject, Criteria
from datetime import datetime

# Compare types of atributes in object and field types in models
TYPES_MAP = {
    int: IntegerField,
    str: TextField,
    bool: BooleanField,
    datetime: DateField,
}


def convert_object_field_to_db_field(field_value):
    '''OLD: Generate value for DB field from corresponding object field'''
    db_value = None
    if type(field_value) is int:
        db_value = int(field_value)
    elif type(field_value) is str:
        db_value = "'" + field_value + "'"
    elif type(field_value) is bool:
        db_value = int(field_value)
    elif field_value is None:
        db_value = 'NULL'
    else:
        raise Exception('Unsupport type %s' % field_value)

    return db_value


def _is_compatible(lg_type, db_type):
    return TYPES_MAP[lg_type] == db_type


class BaseTable:
    __table_name__ = None
    __mapper__ = SQLiteMapper()

    def get_class(self):
        return self._cls

    @classmethod
    def get_column_list(cls):
        column_list = []
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, BaseField):
                column_name = attr_value.column_name if attr_value.column_name else attr_name
                column_list.append(column_name)

        return column_list

    @classmethod
    def get_table_name(cls):
        return cls.__table_name__

    @classmethod
    def get_column_for_field(cls, field_name: str):
        column_name = None
        if field_name not in cls.__dict__:
            raise Exception('Column %s does not exist' % field_name)
        else:
            column_name = cls.__dict__[field_name].column_name
            if not column_name:
                column_name = field_name

        return column_name

    @classmethod
    def construct_select_statement(cls, filter_dict={}, operator='AND', search_like=False):
        _class = cls.__dict__
        table_name = cls.__table_name__

        if not filter_dict:  # Get all
            sql_string = 'SELECT * FROM %s' % table_name
        else:
            sql_string = 'SELECT * FROM %s WHERE ' % table_name
            checked_filter_dict = {}
            # Check fields in filter compatible
            sql_string_list = []
            for attr_name, attr_value in filter_dict.items():
                if attr_name in _class and _is_compatible(
                        type(attr_value), type(_class[attr_name])):
                    checked_filter_dict[attr_name] = attr_value
                    if search_like:
                        db_value = convert_object_field_to_db_field(attr_value)
                        if type(db_value) is str:
                            db_value = "'" + db_value.replace("'", "%") + "'"
                            sql_string_list.append(
                                "%s like %s" % (attr_name, db_value))
                    else:
                        sql_string_list.append(
                            '%s=%s' % (attr_name, convert_object_field_to_db_field(attr_value)))

            # Concat every field values in condition
            sql_string += (' %s ' % operator).join(sql_string_list)

        if 'WHERE' in sql_string[-6:]:
            sql_string = sql_string[:-6]
        return sql_string

    def _check_table_exists(self):
        table_name = self.__class__.__table_name__
        db = Database.get_db_instance()
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';" % table_name
        print(query)
        cursor = db.cursor()
        table_existed = cursor.execute(query).fetchone()
        return table_existed

    def save(self):
        _object_dict = self.__dict__
        _class_attr_dict = {}
        for attr_name, attr_value in self.__class__.__dict__.items():
            if isinstance(attr_value, BaseField):
                _class_attr_dict[attr_name] = attr_value

        obj_dict_to_save = {}
        # Check each attribute of object and compare with class fields, if compatible get it
        for attr_name, attr_value in _object_dict.items():
            if attr_name in _class_attr_dict and _is_compatible(
                    type(_object_dict[attr_name]), type(_class_attr_dict[attr_name])):
                obj_dict_to_save[attr_name] = attr_value

        # Populate default values for non-primary key field
        for attr_name in _class_attr_dict:
            if attr_name not in obj_dict_to_save and not _class_attr_dict[attr_name].primary_key:
                obj_dict_to_save[attr_name] = _class_attr_dict[attr_name].default

        print('Object to save', obj_dict_to_save)
        if not self._check_table_exists():
            print('Table not existed')
        else:
            # Insert a new row
            BaseTable.__mapper__.insert_object(self.__class__, obj_dict_to_save)

    @classmethod
    def execute_find_old(cls, filter_dict={}, operator='AND', search_like=False):
        sql_str = cls.construct_select_statement(filter_dict, operator, search_like)
        print(sql_str)
        db = Database.get_db_instance()
        cursor = db.cursor()
        results = []
        for db_row in cursor.execute(sql_str).fetchall():
            obj = cls()
            obj.__dict__.update(dict(db_row))
            results.append(obj)

        return results

    @classmethod
    def execute_find(cls, criteria, operator='AND'):
        query_obj = QueryObject(cls, operator)
        query_obj.set_criteria(criteria)
        results = query_obj.execute()
        return results

    @classmethod
    def find(cls, criteria=[], operator='AND', recursive=False):
        results = []
        if not recursive:
            results = cls.execute_find(criteria, operator)
        else:
            for sub_class in cls.__subclasses__():
                results.extend(sub_class.execute_find(criteria, operator))

        return results

    @classmethod
    def find_old(cls, filter_dict={}, operator='AND', recursive=False, search_like=False):
        results = []
        if not recursive:
            results = cls.execute_find_old(filter_dict, operator, search_like)
        else:
            for sub_class in cls.__subclasses__():
                results.extend(sub_class.execute_find_old(filter_dict, operator, search_like))

        return results

    def delete(self):
        obj = self.__dict__
        # Find primary key field
        primary_key_field = None
        for attr_name, attr_value in self.__class__.__dict__.items():
            if isinstance(attr_value, BaseField) and attr_value.primary_key:
                primary_key_field = {'name': attr_name, 'value': obj[attr_name]}
                break

        if not primary_key_field:
            raise Exception('Cannot find primary key')

        criteria = Criteria.equal_to(primary_key_field['name'], primary_key_field['value'])
        BaseTable.__mapper__.delete_objects_where(self.__class__,
                                                  criteria.generate_sql_clause(self.__class__, BaseTable.__mapper__))
