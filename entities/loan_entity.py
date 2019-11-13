from orm import BaseTable
from orm.fields import BaseField, IntergerField, TextField


class LoanEntity(BaseTable):
    __table_name__ = 'Loan'

    id = IntergerField(primary_key=True)
    person_id = TextField()
    person_type = TextField(default='Student')
    lib_item_id = IntergerField()
    lib_item_type = TextField()
    borrow_date = TextField()
    return_date = TextField()
