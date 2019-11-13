from abc import ABCMeta, abstractmethod
from orm import BaseTable
from orm.fields import IntergerField, TextField


class PersonEntity(BaseTable):
    __metaclass__ = ABCMeta


class Borrowable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def borrow(self):
        pass


class Student(PersonEntity, Borrowable):
    __table_name__ = 'Student'

    id = IntergerField(primary_key=True)
    name = TextField()

    def borrow(self):
        print('Borrow')


class Teacher(PersonEntity, Borrowable):
    __table_name__ = 'Teacher'

    id = IntergerField(primary_key=True)
    name = TextField()
    faculty = TextField()

    def borrow(self):
        print('Borrow')
