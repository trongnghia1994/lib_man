from orm.database import Database
from orm import execute_sql
from entities.lib_entity import Book, Journal, LibItem
from entities.loan_entity import Loan
from entities.lib_section_entity import CircularSection, MultimediaSection
from entities.member_entity import Teacher, Student

Database.init_db('lib_man.db')


def init_db():
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Book (id integer primary key autoincrement, title text, description text, author text)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Journal (id integer primary key autoincrement, title text, description text, event text)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS CircularSection (id integer primary key autoincrement, name text, description text, no_items integer)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS MultimediaSection (id integer primary key autoincrement, name text, description text, no_computers integer)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Loan (id integer primary key autoincrement, person_id text, person_type text, lib_item_id integer, lib_item_type text, borrow_date text, return_date text)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Student (id integer primary key autoincrement, name text)')
    execute_sql(
        'CREATE TABLE IF NOT EXISTS Teacher (id integer primary key autoincrement, name text, faculty text)')


def create_test_data():
    # for i in range(10):
    #     book = Book()
    #     book.title = 'Book %s' % i
    #     book.description = 'Description for Book %s' % i
    #     book.author = 'Author %s' % i
    #     book.save()
    #
    #     journal = Journal()
    #     journal.title = 'Journal %s' % i
    #     journal.description = 'Description for Journal %s' % i
    #     journal.event = 'Event %s' % i
    #     journal.save()

    # for i in range(10):
    #     t = Teacher()
    #     t.name = 'Teacher %s' % i
    #     t.faculty = 'Faculty %s' % (i % 3)
    #     t.save()
    #
    #     s = Student()
    #     s.name = 'Student %s' % i
    #     s.save()

    cs = MultimediaSection()
    cs.name = 'Section test'
    cs.number_of_computers = 12
    cs.save()


# init_db()
create_test_data()
