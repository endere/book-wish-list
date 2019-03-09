from flask import request
from flask_restplus import Namespace, Resource
from tables.user import User, db
from sqlalchemy.exc import IntegrityError
from flask_restplus import reqparse
create_parser = reqparse.RequestParser()
create_parser.add_argument('first_name', type=str)
create_parser.add_argument('last_name', type=str)
create_parser.add_argument('email', type=str)
create_parser.add_argument('password', type=str)

update_parser = reqparse.RequestParser()
update_parser.add_argument('new_first_name', type=str)
update_parser.add_argument('new_last_name', type=str)
update_parser.add_argument('new_password', type=str)
update_parser.add_argument('new_email', type=str)
update_parser.add_argument('password', type=str)



delete_parser = reqparse.RequestParser()
delete_parser.add_argument('password', type=str)

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
        return user.json


    @users.expect(delete_parser)
    @error_wrapper
    def delete(self, email):
        user = User.query.filter_by(email=email).first()
        if email == user.email and request.values['password'] == user.password:
            db.session.delete(user)
            db.session.commit()
            return {"Status": "delete success"}
        else:
            return {"Status": "Failed authentication. Password incorrect."}

    @users.expect(update_parser)
    @error_wrapper
    def put(self, email):
        user = User.query.filter_by(email=email).first()
        if email == user.email and request.values['password'] == user.password:
            user.first_name = request.values['new_first_name']
            user.last_name = request.values['new_last_name']
            user.password = request.values['new_password']
            user.email = request.values['new_email']
            db.session.commit()
            return user.json
        else:
            return {"Status": "Failed authentication. Password incorrect."}



@users.route('/')
class UserResource(Resource):
    @users.expect(create_parser)
    @error_wrapper
    def post(self):
        user = User(first_name=request.values['first_name'], last_name=request.values['last_name'], email=request.values['email'], password=request.values['password'])
        db.session.add(user)
        db.session.commit()
        return user.json

