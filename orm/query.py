from .mapper import Mapper, SQLiteMapper


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

    @staticmethod
    def match(field_name: str, value: object):
        return MatchCriteria(field_name, value)

    def generate_sql_clause(self, cls, mapper: Mapper) -> str:
        return cls.get_column_for_field(self._field) + self._sql_operator + str(
            mapper.convert_to_db_value(cls, self._value))


class MatchCriteria(Criteria):
    def __init__(self, field: str, value: object):
        self._field = field
        self._value = value

    def generate_sql_clause(self, cls, mapper: Mapper) -> str:
        return 'UPPER(' + cls.get_column_for_field(self._field) + ') LIKE UPPER(' + str(
            mapper.convert_to_db_value(self._value)) + ')'


class QueryObject:
    def __init__(self, cls, criteria: list = [], operator='AND', recursive=False, mapper_cls=SQLiteMapper):
        self._cls = cls
        self._criteria = criteria
        self._mapper = mapper_cls()
        self._operator = operator
        self._recursive = recursive

    def add_criteria(self, one_criteria: Criteria):
        self._criteria.append(one_criteria)

    def generate_where_clause(self):
        clause_str = ''
        for c in self._criteria:
            if clause_str:
                clause_str += ' %s ' % self._operator

            clause_str += c.generate_sql_clause(self._cls, self._mapper)

        return clause_str

    def _execute(self):
        return self._mapper.find_objects_where(self._cls, self.generate_where_clause())

    def execute(self):
        if self._recursive:
            results = []
            for child_cls in self._cls.__subclasses__():
                child_query_obj = QueryObject(child_cls, self._criteria, self._operator, self._operator)
                results.extend(child_query_obj._execute())
            return results
        else:
            return self._execute()
