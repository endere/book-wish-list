"""Sqlalchemy user model."""

from book_wish_list import db
from tables.wishlist import wishlist_table
from sqlalchemy_utils.types.password import PasswordType


class User(db.Model):
    """
    User model using sqlalchemy.

    id is the primary key.
    Email must be unique.
    Password is automatically encoded in the database.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), unique=False, nullable=False)
    last_name = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), unique=False, nullable=False)
    wishlist = db.relationship('Book', secondary=wishlist_table)

    @property
    def json(self):
        """Property function that returns a json representation of the object."""
        return {
            'type': "user",
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'wishlist': self.wishlist_json
        }

    @property
    def wishlist_json(self):
        """Property function that returns a list of all book json in User's wishlsit."""
        return [book.json for book in self.wishlist]
