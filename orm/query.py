from .base_table import BaseTable
from .fields import BaseField
from .database import Database


class DataMap:
    def __init__(self, cls: BaseTable):
        self._cls = cls

    def get_class(self):
        return self._cls

    def get_column_list(self):
        column_list = []
        for attr_name, attr_value in self._cls.__dict__.items():
            if isinstance(attr_value, BaseField):
                column_list.append(attr_name)

        return column_list

    def get_table_name(self):
        return self._cls.__table_name__

    def get_column_for_field(self, field_name: str):
        if field_name not in self.get_column_list():
            raise Exception('Column %s does not exist' % field_name)

        return field_name

    # Convert type
    @staticmethod
    def get_db_value(field_value):
        '''Generate value for DB field from corresponding object field'''
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


class Criteria:
    def __init__(self, sql_operator: str, field: str, value: object):
        self._sql_operator = sql_operator
        self._field = field
        self._value = value

    @staticmethod
    def greater_than(field_name: str, value: object):
        return Criteria('>', field_name, value)

    @staticmethod
    def equal_to(field_name: str, value: object):
        return Criteria('=', field_name, value)

    def generate_sql_clause(self, data_map: DataMap) -> str:
        return data_map.get_column_for_field(self._field) + self._sql_operator + str(DataMap.get_db_value(self._value))


class MatchCriteria(Criteria):
    def __init__(self, field: str, value: object):
        self._field = field
        self._value = value

    def generate_sql_clause(self, data_map: DataMap) -> str:
        return 'UPPER(' + data_map.get_column_for_field(self._field) + ') LIKE UPPER(' + str(
            DataMap.get_db_value(self._value)) + ')'


class QueryObject:
    def __init__(self, cls: BaseTable, criteria: list = [], operator='AND', recursive=False):
        self._cls = cls
        self._criteria = criteria
        self._data_map = DataMap(cls)
        self._operator = operator
        self._recursive = recursive

    def add_criteria(self, one_criteria: Criteria):
        self._criteria.append(one_criteria)

    def generate_where_clause(self):
        clause_str = ''
        for c in self._criteria:
            if clause_str:
                clause_str += ' %s ' % self._operator

            clause_str += c.generate_sql_clause(self._data_map)

        return clause_str

    def _execute(self):
        mapper = Mapper(self._data_map)
        return mapper.find_objects_where(self.generate_where_clause())

    def execute(self):
        if self._recursive:
            results = []
            for child_cls in self._cls.__subclasses__():
                child_query_obj = QueryObject(child_cls, self._criteria, self._operator, self._operator)
                results.extend(child_query_obj._execute())
            return results
        else:
            return self._execute()


class Mapper:
    def __init__(self, data_map: DataMap):
        self._data_map = data_map

    def find_objects_where(self, where_clause):
        cls = self._data_map.get_class()
        column_list = ','.join(self._data_map.get_column_list())
        sql_str = 'SELECT ' + column_list + ' FROM ' + self._data_map.get_table_name() + ' WHERE ' + where_clause
        print(sql_str)
        db = Database.get_db_instance()
        cursor = db.cursor()
        results = []
        for db_row in cursor.execute(sql_str).fetchall():
            obj = cls()
            obj.__dict__.update(dict(db_row))
            results.append(obj)

        return results

    def delete_objects_where(self, where_clause):
        sql_str = 'DELETE FROM ' + self._data_map.get_table_name() + ' WHERE ' + where_clause
        print(sql_str)
        db = Database.get_db_instance()
        cursor = db.cursor()
        cursor.execute(sql_str)
        db.commit()
        print('Delete successfully')
