from abc import ABCMeta, abstractmethod


class IExporter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_export(self):
        raise NotImplementedError


class FileExporter(IExporter):
    def __init__(self, output_path):
        self.output_path = output_path

    def do_export(self, data):
        with open(self.output_path, 'w') as f:
            for e in data:
                f.write(str(e))
                f.write('\n')


class DBExporter(IExporter):
    def do_export(self):
        raise NotImplementedError
