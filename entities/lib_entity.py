from orm.base_table import BaseTable
from orm.fields import IntegerField, TextField


class LibItem(BaseTable):
    pass


class Book(LibItem):
    __table_name__ = 'Book'

    id = IntegerField(primary_key=True)
    title = TextField()
    description = TextField()
    author = TextField()

    def __str__(self):
        return '%s|%s|%s|%s' % (self.id, self.title, self.description, self.author)


class Journal(LibItem):
    __table_name__ = 'Journal'

    id = IntegerField(primary_key=True)
    title = TextField()
    description = TextField()
    event = TextField()

    def __str__(self):
        return '%s|%s|%s|%s' % (self.id, self.title, self.description, self.event)
