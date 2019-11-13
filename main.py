# -*- coding: utf-8 -*-

import json
from utils.search import SearchUtil, SearchResult, LibEntitySearchHelper
from utils.printer import NPrinter
from utils.exporter import FileExporter
from utils.search import SimpleSearchCondition
from models import DATA

from flask import Flask, request, make_response
from orm import Database
from entities.lib_entity import Book, Journal

app = Flask(__name__)


@app.route('/')
def index():
    query = request.values.get('query')
    operator = request.values.get('operator', 'AND')
    if query:
        search_condition = SimpleSearchCondition({
            'title': query,
            'description': query,
            'author': query,
        }, operator)

    if search_condition:
        nprinter = NPrinter()
        fexporter = FileExporter('exports.txt')
        search_helper = LibEntitySearchHelper()
        search_util = SearchUtil(search_condition, search_helper)

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
    Database.init_db('lib_man.db')
    # Run directly
    # nprinter = NPrinter()
    # fexporter = FileExporter('exports.txt')
    search_condition = SimpleSearchCondition({'title': 'B1'})
    search_helper = LibEntitySearchHelper()
    search_util = SearchUtil(search_condition, search_helper)
    # Fetch data
    data = search_util.do_search()
    print(data)

    # app.run('0.0.0.0', debug=True)
