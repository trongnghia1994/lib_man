from orm import BaseTable
from orm.fields import IntergerField, TextField


class LibSection:
    def __init__(self, id, name='', description=''):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return '%s|%s' % (self.name, self.description)


class CirculationSection(LibSection, BaseTable):
    """The books section with a lot of books arranged into categories"""

    __table_name__ = 'circular_section'

    id = IntergerField(primary_key=True)
    name = TextField()
    description = TextField()
    no_items = IntergerField()


class MultimediaSection(LibSection, BaseTable):
    """The multimedia section with a lot of computers, electronic devices"""

    __table_name__ = 'multimedia_section'

    id = IntergerField(primary_key=True)
    name = TextField()
    description = TextField()
    no_computers = IntergerField()
