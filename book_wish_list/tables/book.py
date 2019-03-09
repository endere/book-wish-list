from book_wish_list import db


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=False, nullable=False)
    author = db.Column(db.String(128), unique=False, nullable=False)
    isbn = db.Column(db.String(128), unique=True, nullable=False)
    date_of_publication = db.Column(db.DateTime, unique=False, nullable=False)
