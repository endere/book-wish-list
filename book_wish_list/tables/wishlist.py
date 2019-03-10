"""Declaration of the wishlist table. A reference table that joins users and books in a many to many relationship."""

from book_wish_list import db

wishlist_table = db.Table('wishlist',
                          db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                          db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
                          )
