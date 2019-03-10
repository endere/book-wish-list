"""Routing and orchestration functions for user views."""

from flask import request
from flask_restplus import Namespace, Resource
from tables.user import User, db
from tables.book import Book
from controllers.parsers import (create_parser, update_parser, delete_parser, wishlist_parser)
from controllers.helper_functions import (api_response, error_wrapper, auth_wrapper)


users = Namespace('users', __name__)


@users.route('/')
class UserHandleWithoutId(Resource):
    """Object for handling requests to '/users/' route without an id attatched."""

    @users.expect(create_parser)
    @error_wrapper
    def post(self):
        """
        Create a user in the database with given metadata.

        Then returns the result of the GET with that user's id.
        """
        user = User(first_name=request.values['first_name'], last_name=request.values['last_name'], email=request.values['email'], password=request.values['password'])
        db.session.add(user)
        db.session.commit()
        return UserHandleWithId().get(user.id)

    @error_wrapper
    def get(self):
        """Return list of all users."""
        return api_response(User.query.all(), "success")


@users.route('/<id>')
class UserHandleWithId(Resource):
    """Object for handling requests to '/users/<id>' route, where an id is provided."""

    @error_wrapper
    def get(self, id):
        """
        Return json of a single user of given id.

        Returns not found error if user is not found.
        """
        user = User.query.filter_by(id=id).first()
        return api_response(user.json, "success")

    @users.expect(delete_parser)
    @error_wrapper
    @auth_wrapper
    def delete(self, user):
        """
        Delete a given user from database then return success message.

        Returns authorization error if User's password is not provided.
        Returns not found error if user is not found.
        """
        db.session.delete(user)
        db.session.commit()
        return api_response(None, "success")

    @users.expect(update_parser)
    @error_wrapper
    @auth_wrapper
    def put(self, user):
        """
        Update a given user in database with new metadata then return json for that User.

        Returns authorization error if User's password is not provided.
        Returns not found error if user is not found.
        """
        user.first_name = request.values['new_first_name']
        user.last_name = request.values['new_last_name']
        user.password = request.values['new_password']
        user.email = request.values['new_email']
        db.session.commit()
        return self.get(user.id)


@users.route('/wishlist/<id>')
class WishlistHandle(Resource):
    """Object for handling requests to '/users/wishlist/<id>' route, where a user id is provided."""

    @users.expect(wishlist_parser)
    @error_wrapper
    @auth_wrapper
    def put(self, user):
        """
        Add book of given id to  user's wishlist, then return user's json.

        Returns a not found error if user or book is not found.
        Returns authorization error if User's password is not provided.
        """
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
        """
        Remove book of given id from  user's wishlist, then return user's json.

        Returns a not found error if user or book is not found.
        Returns authorization error if User's password is not provided.
        """
        book = Book.query.filter_by(id=request.values['book_id']).first()
        if not book:
            raise AttributeError
        user.wishlist.remove(book)
        db.session.commit()
        return UserHandleWithId().get(user.id)
