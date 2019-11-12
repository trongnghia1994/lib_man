from orm import BaseTable
from orm.fields import IntergerField, TextField


class LibItem:
    def __init__(self):
        pass


class Book(LibItem, BaseTable):
    __table_name__ = 'Book'

    id = IntergerField()
    title = TextField()
    description = TextField()
    author = TextField()

    def __str__(self):
        return '%s|%s|%s|%s' % (self.type, self.title, self.description, self.author)


class Journal(LibItem, BaseTable):
    __table_name__ = 'Journal'

    id = IntergerField()
    title = TextField()
    description = TextField()
    event = TextField()

    def __str__(self):
        return '%s|%s|%s|%s' % (self.type, self.title, self.description, self.event)
