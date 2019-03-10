from flask import request, abort, url_for, redirect
from flask_restplus import Namespace, Resource
from tables.user import User, db
from tables.book import Book
from controllers.parsers import (create_parser, update_parser, delete_parser, wishlist_parser)
from controllers.helper_functions import (api_response, error_wrapper, auth_wrapper)
users = Namespace('users', __name__)


@users.route('/')
class UserHandleWithoutId(Resource):
    @users.expect(create_parser)
    @error_wrapper
    def post(self):
        user = User(first_name=request.values['first_name'], last_name=request.values['last_name'], email=request.values['email'], password=request.values['password'])
        db.session.add(user)
        db.session.commit()
        return UserHandleWithId().get(user.id)

    @error_wrapper
    def get(self):
        return api_response(User.query.all(), "success")

@users.route('/<id>')
class UserHandleWithId(Resource):

    @error_wrapper
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return api_response(user.json, "success")


    @users.expect(delete_parser)
    @error_wrapper
    @auth_wrapper
    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
        print('heere deleting')
        return api_response(None, "success")


    @users.expect(update_parser)
    @error_wrapper
    @auth_wrapper
    def put(self, user):
        user.first_name = request.values['new_first_name']
        user.last_name = request.values['new_last_name']
        user.password = request.values['new_password']
        user.email = request.values['new_email']
        db.session.commit()
        return self.get(user.id)


@users.route('/wishlist/<id>')
class WishlistHandle(Resource):


    @users.expect(wishlist_parser)
    @error_wrapper
    @auth_wrapper
    def put(self, user):
        book = Book.query.filter_by(id=request.values['book_id']).first()
        if not book:
            raise AttributeError
        user.wishlist.append(book)
        db.session.commit()
        return UserHandleWithId().get(user.id)

    @users.expect(wishlist_parser)
    @error_wrapper
    @auth_wrapper
    def delete(self, user):
        book = Book.query.filter_by(id=request.values['book_id']).first()
        if not book:
            raise AttributeError
        user.wishlist.remove(book)
        db.session.commit()
        return UserHandleWithId().get(user.id)
