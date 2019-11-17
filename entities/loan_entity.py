from orm.base_table import BaseTable
from orm.fields import IntegerField, TextField, DateField


class Loan(BaseTable):
    __table_name__ = 'Loan'

    id = IntegerField(primary_key=True)
    person_id = IntegerField()
    person_type = TextField(default='Student')
    lib_item_id = IntegerField()
    lib_item_type = TextField()
    borrow_date = DateField()
    return_date = DateField()
