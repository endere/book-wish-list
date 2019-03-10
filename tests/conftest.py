"""Fixtures for testing book_wish_list."""
import os
import sys
import json
import pytest
from test_helpers import clear_data

ROOT_DIR = os.path.dirname(os.path.abspath('book_wish_list'))
sys.path.insert(0, ROOT_DIR)

from book_wish_list import app, db

clear_data(db)


@pytest.fixture(scope="session")
def client():
    """A test client for making requests to the app."""
    return app.test_client()


@pytest.fixture(scope="session")
def sample_book(client):
    """
    A book object for use in testing, ideal for repeatedly using the same id.

    Creates the book the first time it is called, then will always return the json of that book. Changes made are permenant.
    """
    data = {
        'title': 'A Darker Shade of Magic', 'author': 'V. E. Schwab', 'isbn': '0765376466', 'date_of_publication': '2016-01-19 00:00:00'
    }
    res = client.post('/books/', data=data)
    loaded_data = json.loads(res.data)
    return loaded_data


@pytest.fixture(scope="session")
def sample_user(client):
    """
    A user object for use in testing, ideal for repeatedly using the same id.

    Creates the user the first time it is called, then will always return the json of that user. Changes made are permenant.
    """
    data = {
        'first_name': 'Steve', 'last_name': 'Williams', 'email': 'steve_williams@generic.email', 'password': 'p4$$VV0RD'
    }
    res = client.post('/users/', data=data)
    loaded_data = json.loads(res.data)
    return loaded_data
