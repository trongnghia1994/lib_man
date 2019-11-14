# -*- coding: utf-8 -*-

import json

from flask import Flask, request, make_response, abort

from entities.lib_entity import Book, Journal, LibItem
from entities.loan_entity import LoanEntity
from orm import Database
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
        data = LibItem.find(recursive=True)
        for d in data:
            d.type = d.__class__.__name__

    response = make_response(json.dumps(data, default=lambda o: o.__dict__))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/', methods=['DELETE'])
def delete():
    id = request.values.get('id')
    type = request.values.get('type')
    if not id:
        return abort(400)

    if type == 'Book':
        data = Book.find({'id': id})
    elif type == 'Journal':
        data = Journal.find({'id': id})
    else:
        raise Exception('Type not supported')

    for obj in data:
        obj.delete()

    response = make_response(json.dumps({'msg': 'Successfully'}, default=lambda o: o.__dict__))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/', methods=['POST'])
def create():
    data = request.json
    if not data:
        return abort(400)

    if data['type'] == 'Book':
        book = Book()
        book.title = data['title']
        book.title = data['description']
        book.title = data['author']
        book.save()
    elif data['type'] == 'Journal':
        journal = Journal()
        journal.title = data['title']
        journal.description = data['description']
        journal.event = data['event']
        journal.save()

    response = make_response(json.dumps({'msg': 'Successfully'}, default=lambda o: o.__dict__))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/loan')
def loan():
    lib_item_id = request.values.get('id')
    lib_item_type = request.values.get('type')

    if not lib_item_id or not lib_item_type:
        return abort(400)

    loan = LoanEntity()
    loan.lib_item_id = lib_item_id
    loan.lib_item_type = lib_item_type
    loan.person_id = int(1)
    loan.borrow_date = '13-11-2019'
    loan.return_date = '15-11-2019'
    loan.save()

    response = make_response(json.dumps({'msg': 'Successfully'}, default=lambda o: o.__dict__))
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

    app.run('0.0.0.0', debug=True)
