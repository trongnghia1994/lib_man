from abc import ABCMeta, abstractmethod
from .exporter import IExporter
from .printer import IPrinter


class SearchHelper:
    __metaclass__ = ABCMeta

    def set_conditions(self, conditions):
        self.conditions = conditions

    def set_data(self, data):
        self.data = data

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class LibEntitySearchHelper(SearchHelper):
    def __init__(self):
        SearchHelper.__init__(self)

    def __field_satisfied(self, data_field, input):
        if not data_field:
            return False
        return input.lower() in data_field.lower()

    def execute(self):
        results = []
        for data_item in self.data:
            satisfied = False
            for field in self.conditions:
                if self.__field_satisfied(getattr(data_item, field, None), self.conditions[field]):
                    satisfied = True
                    break

            if satisfied:
                results.append(data_item)

        return results


class SearchUtil:
    def __init__(self, conditions: dict, search_helper: SearchHelper, data):
        self.results = []
        self.conditions = conditions
        self.search_helper = search_helper
        self.search_helper.set_conditions(conditions)
        self.search_helper.set_data(data)

    def do_search(self):
        return self.search_helper.execute()


class SearchResult:
    def __init__(self, printer: IPrinter, exporter: IExporter):
        self.printer = printer
        self.exporter = exporter

    def get_results(self, results):
        self.printer.do_print(results)
        self.exporter.do_export(results)
