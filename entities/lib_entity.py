class LibItem:
    def __init__(self, id, title='', description=''):
        self.id = id
        self.title = title
        self.description = description


class Book(LibItem):
    def __init__(self, id='', title='', description='', author=''):
        LibItem.__init__(self, id, title, description)
        self.author = author
        self.type = 'Book'

    def __str__(self):
        return '%s|%s|%s|%s' % (self.type, self.title, self.description, self.author)


class Journal(LibItem):
    def __init__(self, id='', title='', description='', event=''):
        LibItem.__init__(self, id, title, description)
        self.event = event
        self.type = 'Journal'

    def __str__(self):
        return '%s|%s|%s|%s' % (self.type, self.title, self.description, self.event)
