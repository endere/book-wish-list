from book_wish_list import db
from tables.wishlist import wishlist_table



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), unique=False, nullable=False)
    last_name = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.DateTime, unique=False, nullable=False)
    books = db.relationship('Book', secondary=wishlist_table)
