from abc import ABCMeta, abstractmethod


class IPrinter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_print(self):
        pass


class NPrinter(IPrinter):
    def do_print(self, data):
        for e in data:
            print(e)


class APrinter(IPrinter):
    def do_print(self, data):
        for e in data:
            print(type(e), e)
