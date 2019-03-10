from flask import request
from flask_restplus import Namespace, Resource
from tables.user import User, db
from tables.book import Book
from controllers.parsers import (create_parser, update_parser, delete_parser, wishlist_parser)
from controllers.helper_functions import (api_response, error_wrapper, auth_wrapper)
users = Namespace('users', __name__)



@users.route('/')
class UserPost(Resource):
    @users.expect(create_parser)
    @error_wrapper
    def post(self):
        user = User(first_name=request.values['first_name'], last_name=request.values['last_name'], email=request.values['email'], password=request.values['password'])
        db.session.add(user)
        db.session.commit()
        return api_response(user, "Create User success")

    def get(self):
        return api_response(User.query.all(), "Get User list success")

@users.route('/<id>')
class UserHandle(Resource):

    @error_wrapper
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return api_response(user, "get User success")


    @users.expect(delete_parser)
    @error_wrapper
    @auth_wrapper
    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
        return api_response(None, "Delete User success")


    @users.expect(update_parser)
    @error_wrapper
    @auth_wrapper
    def put(self, user):
        user.first_name = request.values['new_first_name']
        user.last_name = request.values['new_last_name']
        user.password = request.values['new_password']
        user.email = request.values['new_email']
        db.session.commit()
        return api_response(user, "Update User success")



@users.route('/wishlist/<id>')
class WishlistHandle(Resource):

    @error_wrapper
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return user.wishlist

    @users.expect(wishlist_parser)
    @error_wrapper
    @auth_wrapper
    def put(self, user):
        book = Book.query.filter_by(id=request.values['book_id']).first()
        user.wishlist.append(book)
        db.session.commit()
        return api_response(user, "Book added to wishlist")

    @users.expect(wishlist_parser)
    @error_wrapper
    @auth_wrapper
    def delete(self, user):
        book = Book.query.filter_by(id=request.values['book_id']).first()
        user.wishlist.remove(book)
        db.session.commit()
        return api_response(user, "Book deleted from wishlist")

