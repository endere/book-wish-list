"""Routing and orchestration functions for book views."""

from flask import request
from flask_restplus import Namespace, Resource
from controllers.parsers import (book_create_parser, book_update_parser)
from tables.book import Book, db
from tables.wishlist import wishlist_table
from controllers.helper_functions import (api_response, error_wrapper)


books = Namespace('books', __name__)


@books.route('/')
class BookHandleWithoutId(Resource):
    """Object for handling requests to '/books/' route without an id attatched."""

    @books.expect(book_create_parser)
    @error_wrapper
    def post(self):
        """
        Create a book in the database with given metadata.

        Then returns the result of the GET with that book's id.
        """
        book = Book(title=request.values['title'], author=request.values['author'], isbn=request.values['isbn'], date_of_publication=request.values['date_of_publication'])
        db.session.add(book)
        db.session.commit()
        return BookHandleWithId().get(book.id)

    @error_wrapper
    def get(self):
        """Return a list of all books."""
        return api_response(Book.query.all(), "success")


@books.route('/<id>')
class BookHandleWithId(Resource):
    """Object for handling requests to '/books/<id>' route with an id attatched."""

    @error_wrapper
    def get(self, id):
        """
        Return json of a single book of given id.

        Returns not found error if book is not found.
        """
        book = Book.query.filter_by(id=id).first()
        return api_response(book.json, "success")

    @error_wrapper
    def delete(self, id):
        """
        Delete a given book from database then return success message.

        Returns not found error if book is not found.
        Return 'cannot remove' error if book is listed in a User's wishlist.
        """
        book = Book.query.filter_by(id=id).first()
        if not book:
            raise AttributeError
        if db.session.query(wishlist_table).filter(wishlist_table.c.book_id == id).count():
            return api_response(None, "Cannot remove due to book existing in at least one user's wishlist", 400)
        else:
            db.session.delete(book)
            db.session.commit()
            return api_response(None, "success")

    @books.expect(book_update_parser)
    @error_wrapper
    def put(self, id):
        """
        Update a given book in database with new metadata then return json for that book.

        Returns not found error if book is not found.
        """
        book = Book.query.filter_by(id=id).first()
        if not book:
            raise AttributeError
        book.title = request.values['new_title']
        book.author = request.values['new_author']
        book.isbn = request.values['new_isbn']
        book.date_of_publication = request.values['new_date_of_publication']
        db.session.commit()
        return self.get(book.id)
