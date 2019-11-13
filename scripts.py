from orm.database import Database
from orm import execute_sql
from entities.lib_entity import Book, Journal, LibItem

Database.init_db('lib_man.db')


def init_db():
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Book (id int integer primary key, title text, description text, author text)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Journal (id int integer primary key, title text, description text, event text)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS CircularSection (id int integer primary key, name text, description text, no_items integer)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS MultimediaSection (id int integer primary key, title text, description text, no_computers integer)')


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


create_test_data()
# Test find
results = LibItem.find({'title': 'B3'}, recursive=True)
print([(r.id, r.title) for r in results])
