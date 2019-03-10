"""Sqlalchemy user model."""

from book_wish_list import db


class Book(db.Model):
    """
    User model using sqlalchemy.

    id is the primary key.
    isbn must be unique.
    """

    __tablename__ = 'books'
    id = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    title = db.Column(db.String(128), unique=False, nullable=False)
    author = db.Column(db.String(128), unique=False, nullable=False)
    isbn = db.Column(db.String(128), unique=True, nullable=False)
    date_of_publication = db.Column(db.DateTime, unique=False, nullable=False)

    @property
    def json(self):
        """Property function that returns a json representation of the object."""
        return {
            'type': "book",
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'date_of_publication': str(self.date_of_publication)
        }
