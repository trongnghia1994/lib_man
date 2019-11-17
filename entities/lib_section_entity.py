from orm.base_table import BaseTable
from orm.fields import IntegerField, TextField


class LibSection(BaseTable):
    pass


class CircularSection(LibSection):
    """The books section with a lot of books arranged into categories"""

    __table_name__ = 'CircularSection'

    id = IntegerField(primary_key=True)
    name = TextField()
    description = TextField()
    number_of_items = IntegerField(column_name='no_items')

    def __str__(self):
        return '%s|%s|%s|%s' % (self.id, self.name, self.description, self.no_items)


class MultimediaSection(LibSection):
    """The multimedia section with a lot of computers, electronic devices"""

    __table_name__ = 'MultimediaSection'

    id = IntegerField(primary_key=True)
    name = TextField()
    description = TextField()
    number_of_computers = IntegerField(column_name='no_computers')

    def __str__(self):
        return '%s|%s|%s|%s' % (self.id, self.name, self.description, self.no_computers)
