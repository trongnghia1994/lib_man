from abc import ABCMeta, abstractmethod
from orm.base_table import BaseTable
from orm.fields import IntegerField, TextField
from entities.lib_entity import LibItem
from entities.loan_entity import Loan
from datetime import datetime


class MemberEntity(BaseTable):
    __metaclass__ = ABCMeta


class Borrowable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def borrow(self, lib_item: LibItem, return_date: datetime):
        pass


class Student(MemberEntity, Borrowable):
    __table_name__ = 'Student'

    id = IntegerField(primary_key=True)
    name = TextField()

    def borrow(self, lib_item: LibItem, return_date: datetime):
        loan = Loan()
        loan.lib_item_id = lib_item.id
        loan.lib_item_type = lib_item.__class__.__name__
        loan.person_id = self.id
        loan.person_type = self.__class__.__name__
        loan.borrow_date = datetime.now()
        loan.return_date = return_date
        loan.save()
        print('Save loan data successfully')


class Teacher(MemberEntity, Borrowable):
    __table_name__ = 'Teacher'

    id = IntegerField(primary_key=True)
    name = TextField()
    faculty = TextField()

    def borrow(self, lib_item: LibItem, return_date: datetime):
        loan = Loan()
        loan.lib_item_id = lib_item.id
        loan.lib_item_type = lib_item.type
        loan.person_id = self.id
        loan.person_type = self.__class__.__name__
        loan.borrow_date = datetime.now()
        loan.return_date = return_date
        loan.save()
        print('Save loan data successfully')
