# -*- coding: utf-8 -*-

import json
from utils.search import SearchUtil, SearchResult, LibEntitySearchHelper
from utils.printer import NPrinter
from utils.exporter import FileExporter
from models import DATA

from flask import Flask, request, make_response
from orm import Database
from entities.lib_entity import Book, Journal

app = Flask(__name__)


@app.route('/')
def index():
    search_conditions = {}
    query = request.values.get('query')
    if query:
        search_conditions = {
            'title': query,
            'description': query,
            'author': query,
        }

    if search_conditions:
        nprinter = NPrinter()
        fexporter = FileExporter('exports.txt')
        search_helper = LibEntitySearchHelper()
        search_util = SearchUtil(search_conditions, search_helper, DATA)

        # Fetch data
        data = search_util.do_search()

        # Export and print
        search_result = SearchResult(nprinter, fexporter)
        search_result.get_results(data)
    else:
        data = DATA

    response = make_response(json.dumps(data, default=lambda o: o.__dict__))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    # Run directly
    # nprinter = NPrinter()
    # fexporter = FileExporter('exports.txt')
    # conditions = {'title': 'Truyen ngan'}
    # search_util = LibEntitySearchUtil()
    # search_result = SearchResult(conditions, search_util, DATA, nprinter, fexporter)
    # search_result.do_search()
    # search_result.get_results()

    # Some examples of ORM
    Database.init_db('lib_man.db')
    # print(cursor.execute('SELECT * from book').fetchall())
    # book = Book()
    # book.id = 3
    # book.title = 'B3'
    # book.description = 'D3'
    # book.author = 'SGK'
    # book.save()

    # TODO Handle default values of columns, primary keys...
    # journal = Journal()
    # journal.id = 1
    # journal.title = 'J1'
    # journal.description = 'J1'
    # journal.event = 'HCM Journal'
    # journal.save()
    # for row in Book.find({'title': 'B2', 'id': 1}, operator='OR'):
    #     print(row['id'])

    journals = Journal.find({'title': 'J1', 'id': 1})
    for row in journals:
        print(row['id'], row['title'])
