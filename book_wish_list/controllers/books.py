import json
from flask import abort, Blueprint, render_template, request
from flask_restplus import Namespace, Resource, fields
from controllers.parsers import (book_create_parser, book_update_parser)
from tables.book import Book, db
from tables.wishlist import wishlist_table
from controllers.helper_functions import (api_response, error_wrapper)


books = Namespace('books', __name__)




@books.route('/')
class BookPost(Resource):
    @books.expect(book_create_parser)
    @error_wrapper
    def post(self):
        book = Book(title=request.values['title'], author=request.values['author'], isbn=request.values['isbn'], date_of_publication=request.values['date_of_publication'])
        db.session.add(book)
        db.session.commit()
        return api_response(book, "Create success")

    def get(self):
        return api_response(Book.query.all(), "Get success")

@books.route('/<id>')
class BookHandle(Resource):

    @error_wrapper
    def get(self, id):
        book = Book.query.filter_by(id=id).first()
        return api_response(book, "get success")

    @error_wrapper
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        if db.session.query(wishlist_table).filter(wishlist_table.c.book_id==id).count():
            return api_response(book, "Cannot remove due to book existing in at least one user's wishlist")
        else:
            db.session.delete(book)
            db.session.commit()
            return api_response(None, "Delete success")

    @books.expect(book_update_parser)
    def put(self, id):
        book = Book.query.filter_by(id=id).first()
        book.title = request.values['new_title']
        book.author = request.values['new_author']
        book.isbn = request.values['new_isbn']
        book.date_of_publication = request.values['new_date_of_publication']
        db.session.commit()
        return api_response(book, "Update success")
