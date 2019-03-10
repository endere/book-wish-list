import json
from flask import abort, Blueprint, render_template, request
from flask_restplus import Namespace, Resource, fields
from controllers.parsers import (book_create_parser, book_update_parser)
from tables.book import Book, db
from tables.wishlist import wishlist_table
from controllers.helper_functions import (api_response, error_wrapper)


books = Namespace('books', __name__)


@books.route('/')
class BookHandleWithoutId(Resource):
    @books.expect(book_create_parser)
    @error_wrapper
    def post(self):
        book = Book(title=request.values['title'], author=request.values['author'], isbn=request.values['isbn'], date_of_publication=request.values['date_of_publication'])
        db.session.add(book)
        db.session.commit()
        return BookHandleWithId().get(book.id)

    def get(self):
        return api_response(Book.query.all(), "success")

@books.route('/<id>')
class BookHandleWithId(Resource):

    @error_wrapper
    def get(self, id):
        print('in get')
        book = Book.query.filter_by(id=id).first()
        return api_response(book.json, "success")

    @error_wrapper
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        if not book:
            raise AttributeError
        if db.session.query(wishlist_table).filter(wishlist_table.c.book_id==id).count():
            return api_response(None, "Cannot remove due to book existing in at least one user's wishlist", 400)
        else:
            db.session.delete(book)
            db.session.commit()
            return api_response(None, "success")

    @books.expect(book_update_parser)
    @error_wrapper
    def put(self, id):
        book = Book.query.filter_by(id=id).first()
        if not book:
            raise AttributeError
        book.title = request.values['new_title']
        book.author = request.values['new_author']
        book.isbn = request.values['new_isbn']
        book.date_of_publication = request.values['new_date_of_publication']
        db.session.commit()
        return self.get(book.id)
