from .database import Database
from .fields import BaseField, IntergerField, TextField, BooleanField

# Compare types of atributes in object and field types in models
TYPES_MAP = {
    int: IntergerField,
    str: TextField,
    bool: BooleanField,
}


# Convert type
def convert_object_field_to_db_field(obj_field_value):
    '''Generate value for DB field from corresponding object field'''
    db_value = None
    if type(obj_field_value) is int:
        db_value = int(obj_field_value)
    elif type(obj_field_value) is str:
        db_value = "'" + obj_field_value + "'"
    elif type(obj_field_value) is bool:
        db_value = int(obj_field_value)
    elif obj_field_value is None:
        db_value = 'NULL'
    else:
        raise Exception('Unsupport type %s' % obj_field_value)

    return db_value


def _is_compatible(lg_type, db_type):
    return TYPES_MAP[lg_type] == db_type


class BaseTable:
    __table_name__ = None

    def construct_insert_statement(self, obj_attr_dict):
        '''Construct SQL insert statement from object attributes dict'''
        table_name = self.__class__.__table_name__
        if len(obj_attr_dict) == 0:
            raise Exception('Object attributes null')
        sql_fields_str = ''
        for attr_value in obj_attr_dict.values():
            db_field_value = convert_object_field_to_db_field(attr_value)
            # Concat the fields' values
            if type(db_field_value) is int:
                sql_fields_str += str(db_field_value)
            elif type(db_field_value) is str:
                sql_fields_str += db_field_value

            sql_fields_str += ','

        if sql_fields_str[-1] == ',':
            sql_fields_str = sql_fields_str[:-1]

        if sql_fields_str:
            fields_to_insert = ','.join(obj_attr_dict.keys())
            sql_string = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, fields_to_insert, sql_fields_str)
            return sql_string
        else:
            raise Exception('Object attributes null')

    def construct_delete_statement(self, primary_key_field):
        '''Construct SQL insert statement from object attributes dict'''
        table_name = self.__class__.__table_name__

        db_field_value = convert_object_field_to_db_field(primary_key_field['value'])
        return 'DELETE FROM %s WHERE %s = %s' % (table_name, primary_key_field['name'], db_field_value)

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
                        sql_string_list.append('%s=%s' % (attr_name, convert_object_field_to_db_field(attr_value)))

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
        _object = self.__dict__
        _class = {}
        for attr_name, attr_value in self.__class__.__dict__.items():
            if isinstance(attr_value, BaseField):
                _class[attr_name] = attr_value

        obj_to_save = {}
        # Check attribute of object and compare with class fields, if same get it
        for attr_name, attr_value in _object.items():
            if attr_name in _class and _is_compatible(
                    type(_object[attr_name]), type(_class[attr_name])):
                obj_to_save[attr_name] = attr_value

        # Populate default values for non-primary key field
        for attr_name in _class:
            if attr_name not in obj_to_save and not _class[attr_name].primary_key:
                obj_to_save[attr_name] = _class[attr_name].default

        print('Object to save', obj_to_save)
        if not self._check_table_exists():
            # Create table here
            print('Table not existed')
        else:
            # Insert a new row
            sql_str = self.construct_insert_statement(obj_to_save)
            print(sql_str)
            db = Database.get_db_instance()
            cursor = db.cursor()
            cursor.execute(sql_str)
            db.commit()
            print('Insert successfully')

    @classmethod
    def _find(cls, filter_dict={}, operator='AND', search_like=False):
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
    def find(cls, filter_dict={}, operator='AND', recursive=False, search_like=False):
        results = []
        if not recursive:
            results = cls._find(filter_dict, operator, search_like)
        else:
            for sub_class in cls.__subclasses__():
                results.extend(sub_class._find(filter_dict, operator, search_like))

        return results

    @classmethod
    def _search(cls, text, recursive=False):
        pass

    @classmethod
    def search(cls, text, recursive=False):
        results = []
        if not recursive:
            results = cls._search(text)
        else:
            for sub_class in cls.__subclasses__():
                results.extend(sub_class._search(text))

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

        sql_str = self.construct_delete_statement(primary_key_field)
        print(sql_str)
        db = Database.get_db_instance()
        cursor = db.cursor()
        cursor.execute(sql_str)
        db.commit()
        print('Delete successfully')
