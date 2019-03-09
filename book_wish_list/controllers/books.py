import json
from flask import abort, Blueprint, render_template, request
from flask_restplus import Namespace, Resource, fields

books = Namespace('books', __name__)


@books.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world2'}

