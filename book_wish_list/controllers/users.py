import json
from flask import abort, Blueprint, render_template, request
from flask_restplus import Namespace, Resource, fields
from tables.user import User, db
from sqlalchemy.exc import IntegrityError
from flask_restplus import reqparse
create_parser = reqparse.RequestParser()
create_parser.add_argument('first_name', type=str)
create_parser.add_argument('last_name', type=str)
create_parser.add_argument('email', type=str)
create_parser.add_argument('password', type=str)

users = Namespace('users', __name__)
def error_wrapper(f):
    """Decorator that parses errors and response codes from controller response."""
    def _wrapper(*args, **kwargs):
        """."""
        try:
            res = f(*args, **kwargs)
        except AttributeError:
            return {'Error': 'Resource not found'}, 404
        except IntegrityError:
            return {'Error': 'Email already exists'}, 400
        return res
    return _wrapper




@users.route('/<email>')
class UserGet(Resource):

    @error_wrapper
    def get(self, email):
        user = User.query.filter_by(email=email).first()
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }


@users.route('/')
class UserResource(Resource):

    @users.expect(create_parser)
    @error_wrapper
    def post(self):
        user = User(first_name=request.values['first_name'], last_name=request.values['last_name'], email=request.values['email'], password=request.values['password'])
        db.session.add(user)
        db.session.commit()
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }



