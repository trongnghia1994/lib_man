# -*- coding: utf-8 -*-

import json

from flask import Flask, request, make_response

from entities.lib_entity import Book, Journal, LibItem
from entities.loan_entity import LoanEntity
from orm.database import Database
from orm.query import QueryObject, Criteria, MatchCriteria
from utils.exporter import FileExporter
from utils.printer import NPrinter
from utils.search import SearchUtil, SearchResult, LibEntitySearchHelper
from utils.search import SimpleSearchCondition

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    query = request.values.get('query')
    operator = request.values.get('operator', 'OR')

    search_condition = None
    if query:
        search_condition = SimpleSearchCondition({
            'title': query,
            'description': query,
            'author': query,
            'event': query,
        }, operator)

    if search_condition:
        nprinter = NPrinter()
        fexporter = FileExporter('exports.txt')
        search_helper = LibEntitySearchHelper()
        search_helper.set_query = query
        search_util = SearchUtil(search_condition, search_helper)

        # Fetch data
        data = search_util.do_search()

        # Export and print
        search_result = SearchResult(nprinter, fexporter)
        search_result.get_results(data)
    else:
        data = LibItem.find_old(recursive=True)
        for d in data:
            d.type = d.__class__.__name__

    response = make_response(json.dumps(data, default=lambda o: o.__dict__))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    Database.init_db('lib_man.db')
    # Run directly
    # nprinter = NPrinter()
    # fexporter = FileExporter('exports.txt')
    # search_condition = SimpleSearchCondition({'title': 'B1'})
    # search_helper = LibEntitySearchHelper()
    # search_util = SearchUtil(search_condition, search_helper)
    # # Fetch data
    # data = search_util.do_search()
    # print(data)
    # app.run('0.0.0.0', debug=True)
    # Insert data
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

    # Find
    query_obj = QueryObject(LoanEntity, recursive=False)
    query_obj.add_criteria(Criteria.greater_than('id', 5))
    # query_obj.add_criteria(Criteria.equal_to('title', 'Book title'))
    # query_obj.add_criteria(MatchCriteria('description', 'Book'))
    results = query_obj.execute()
    for obj in results:
        print(obj)
    # obj_to_del = results[0]
    # print(obj_to_del)
    # obj_to_del.delete()

    # book = Book()
    # book.title = 'Book test 2'
    # book.description = 'Description for Book test 2'
    # book.author = 'Author test 2'
    # book.save()

    # for i in range(10):
    #     loan = LoanEntity()
    #     loan.person_id = 1
    #     loan.person_type = 'Student' if i % 2 == 0 else 'Teacher'
    #     loan.borrow_date = '18-11-2019'
    #     loan.return_date = '28-11-2019'
    #     loan.save()
