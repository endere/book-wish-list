from flask import request, redirect, url_for
from flask_restplus import Namespace, Resource
from tables.user import User, db
from tables.book import Book
from sqlalchemy.exc import IntegrityError
from controllers.parsers import (create_parser, update_parser, delete_parser, wishlist_parser)


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


@users.route('/')
class UserPost(Resource):
    @users.expect(create_parser)
    @error_wrapper
    def post(self):
        user = User(first_name=request.values['first_name'], last_name=request.values['last_name'], email=request.values['email'], password=request.values['password'])
        db.session.add(user)
        db.session.commit()
        return {"status": "Create success", "user": user.json}

@users.route('/<id>')
class UserHandle(Resource):

    @error_wrapper
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {"status": "Get success", "user": user.json}


    @users.expect(delete_parser)
    @error_wrapper
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if int(id) == user.id and request.values['password'] == user.password:
            db.session.delete(user)
            db.session.commit()
            return {"status": "Delete success"}
        else:
            return {"status": "Failed authentication. Password incorrect."}

    @users.expect(update_parser)
    @error_wrapper
    def put(self, id):
        user = User.query.filter_by(id=id).first()
        if int(id) == user.id and request.values['password'] == user.password:
            user.first_name = request.values['new_first_name']
            user.last_name = request.values['new_last_name']
            user.password = request.values['new_password']
            user.email = request.values['new_email']
            db.session.commit()
            return {"status": "Update success", "user": user.json}
        else:
            return {"status": "Failed authentication. Password incorrect."}



@users.route('/wishlist/<id>')
class WishlistHandle(Resource):

    @error_wrapper
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return user.wishlist

    @users.expect(wishlist_parser)
    @error_wrapper
    def put(self, id):
        user = User.query.filter_by(id=id).first()
        book = Book.query.filter_by(isbn=request.values['isbn']).first()
        if not book:
            book = Book(title=request.values['title'], author=request.values['author'], isbn=request.values['isbn'], date_of_publication=request.values['date_of_publication'])
        if int(id) == user.id and request.values['password'] == user.password:
            user.wishlist.append(book)
            db.session.add(book)
            db.session.commit()
            return {"status": "Book added to wishlist", "user": user.json}
        else:
            return {"status": "Failed authentication. Password incorrect."}


