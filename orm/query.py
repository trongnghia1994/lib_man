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
    def less_than_or_equal(field_name: str, value: object):
        return Criteria('<=', field_name, value)

    @staticmethod
    def equal_to(field_name: str, value: object):
        return Criteria('=', field_name, value)

    @staticmethod
    def match(field_name: str, value: object):
        return MatchCriteria(field_name, value)

    def generate_sql_clause(self, cls, mapper_cls) -> str:
        return cls.get_column_for_field(self._field) + self._sql_operator + str(
            mapper_cls.convert_to_db_value(self._value))


class MatchCriteria(Criteria):
    def __init__(self, field: str, value: object):
        self._field = field
        self._value = value

    def generate_sql_clause(self, cls, mapper_cls) -> str:
        pattern_str = "'%" + str(mapper_cls.convert_to_db_value(self._value))[1:-1].upper() + "%'"
        return 'UPPER(' + cls.get_column_for_field(self._field) + ') LIKE ' + pattern_str


class QueryObject:
    def __init__(self, entity_cls, operator='AND', find_children=False, mapper_cls=SQLiteMapper):
        self._entity_cls = entity_cls
        self._criteria = []
        self._mapper_cls = mapper_cls
        self._operator = operator
        self._find_children = find_children

    def set_criteria(self, criteria):
        self._criteria = criteria

    def add_criteria(self, one_criteria: Criteria):
        self._criteria.append(one_criteria)

    def generate_where_clause(self):
        clause_str = ''
        for c in self._criteria:
            if clause_str:
                clause_str += ' %s ' % self._operator

            clause_str += c.generate_sql_clause(self._entity_cls, self._mapper_cls)

        return clause_str

    def _execute(self):
        return self._mapper_cls.find_objects_where(self._entity_cls, self.generate_where_clause())

    def execute(self):
        if self._find_children:
            results = []
            for child_entity_cls in self._entity_cls.__subclasses__():
                child_query_obj = QueryObject(child_entity_cls, self._operator)
                child_query_obj.set_criteria(self._criteria)
                results.extend(child_query_obj._execute())
            return results
        else:
            return self._execute()
