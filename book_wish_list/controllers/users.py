import json
from flask import abort, Blueprint, render_template, request
from flask_restplus import Namespace, Resource, fields
from tables.user import User
users = Namespace('users', __name__)


@users.route('/hello')
class HelloWorld(Resource):
    def get(self):
        print(User)
        return {'hello': 'users view'}

