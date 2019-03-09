import os
import uuid

from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

api = Api(app, doc='/swagger/')

db = SQLAlchemy(app)

for module_name in ['book', 'wishlist', 'user']:
    import_module(f'tables.{module_name}', package=__name__)

from controllers.books import books
from controllers.users import users
api.add_namespace(books)

api.add_namespace(users)


db.create_all()

