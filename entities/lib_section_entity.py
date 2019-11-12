class LibSection:
    def __init__(self, id, name='', description=''):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return '%s|%s' % (self.name, self.description)


class CirculationSection(LibSection):
    def __init__(self, id='', name='', description='', security_staff_name=''):
        LibSection.__init__(self, id, name, description)
        self.security_staff_name = security_staff_name
        self.type = 'CirculationSection'


class MultimediaSection(LibSection):
    def __init__(self, id='', name='', description='', computers=[]):
        MultimediaSection.__init__(self, id, name, description)
        self.computers = computers
        self.type = 'MultimediaSection'
