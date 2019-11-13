from orm.database import Database
from orm import execute_sql
from entities.lib_entity import Book, Journal, LibItem
from entities.loan_entity import LoanEntity

Database.init_db('lib_man.db')


def init_db():
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Book (id integer primary key autoincrement, title text, description text, author text)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Journal (id integer primary key autoincrement, title text, description text, event text)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS CircularSection (id integer primary key autoincrement, name text, description text, no_items integer)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS MultimediaSection (id integer primary key autoincrement, title text, description text, no_computers integer)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Loan (id integer primary key autoincrement, person_id text, person_type text, lib_item_id integer, lib_item_type text, borrow_date text, return_date text)')


def create_test_data():
    book = Book()
    book.id = 6
    book.title = 'How was steel tempered'
    # book.description = 'New Book'
    book.author = 'Nicolai Ostrovski'
    book.save()

    journal = Journal()
    journal.id = 2
    journal.title = 'Privacy Preserving in Open data'
    journal.description = 'A journal in Data Privacy'
    # journal.event = 'HCM Journal'
    journal.save()


# init_db()
# create_test_data()
# Test find
# results = LibItem.find({'id': 6}, recursive=True)
# results[0].delete()
# last_book.delete()
# print([(r.id, r.title) for r in results])

# init_db()
# book = Book()
# # book.id = 6
# book.title = '3 nguoi thay vi dai'
# # book.description = 'New Book'
# book.author = 'N/A'
# book.save()

results = LibItem.find({'id': 1, 'title': 'dai'}, search_like=True, recursive=True)
print(results)
