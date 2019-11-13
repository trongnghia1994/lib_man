from abc import ABCMeta, abstractmethod
from .exporter import IExporter
from .printer import IPrinter
from entities.lib_entity import LibItem


class SearchCondition:
    __metaclass__ = ABCMeta


class SimpleSearchCondition(SearchCondition):
    def __init__(self, fields_data: dict, operator: str = 'AND'):
        self.fields_data = fields_data
        self.operator = operator


class SearchHelper:
    __metaclass__ = ABCMeta

    def set_condition(self, condition: SearchCondition):
        self._condition = condition

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class LibEntitySearchHelper(SearchHelper):
    def __init__(self):
        SearchHelper.__init__(self)

    def execute(self):
        results = LibItem.find(self._condition.fields_data, self._condition.operator, recursive=True)
        return results


class SearchUtil:
    def __init__(self, condition: SearchCondition, search_helper: SearchHelper):
        self.results = []
        self.condition = condition
        self.search_helper = search_helper
        self.search_helper.set_condition(condition)

    def do_search(self):
        return self.search_helper.execute()


class SearchResult:
    def __init__(self, printer: IPrinter, exporter: IExporter):
        self.printer = printer
        self.exporter = exporter

    def get_results(self, results):
        self.printer.do_print(results)
        self.exporter.do_export(results)
