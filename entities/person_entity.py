from abc import ABCMeta, abstractmethod


class PersonEntity:
    __metaclass__ = ABCMeta


class Borrowable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def borrow(self):
        pass


class BookManageable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def manage(self):
        pass


class Student(PersonEntity, Borrowable):
    def borrow(self):
        print('Borrow')


class Librarian(PersonEntity, BookManageable):
    def manage(self):
        print('Manage')
