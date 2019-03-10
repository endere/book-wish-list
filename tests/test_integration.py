from __future__ import absolute_import
from clear_data import clear_data
import os
import sys
import json
from copy import deepcopy

from flask import Flask
import os
import tempfile

import pytest

ROOT_DIR = os.path.dirname(os.path.abspath('book_wish_list'))
sys.path.insert(0, ROOT_DIR)

from book_wish_list import app, db
clear_data(db)

@pytest.fixture(scope="session")
def client():
    return app.test_client()

@pytest.fixture(scope="session")
def sample_book(client):
    data = {
        'title': 'A Darker Shade of Magic', 'author': 'V. E. Schwab', 'isbn': '0765376466', 'date_of_publication': '2016-01-19 00:00:00'
    }
    res = client.post('/books/', data=data)
    loaded_data = json.loads(res.data)
    return loaded_data

def verify_model(loaded_data, expected, model_type):
    for key in expected:
        if key == 'password':
            continue
        assert loaded_data[key] == expected[key]
    assert loaded_data['type'] == model_type
    if 'wishlist' in loaded_data:
        for i in range(len(expected['wishlist'])):
            verify_model(loaded_data['wishlist'][i], expected['wishlist'][i], 'book')


@pytest.fixture(scope="session")
def sample_user(client):
    data = {
        'first_name': 'Steve', 'last_name': 'Williams', 'email': 'steve_williams@generic.email', 'password': 'p4$$VV0RD'
    }
    res = client.post('/users/', data=data)
    loaded_data = json.loads(res.data)
    return loaded_data


def test_empty_book_list_returns_empty_data(client):
    res = client.get('/books/')
    assert json.loads(res.data) == {
        "status": "success",
        "data": []
    }
    assert res.status_code == 200

def test_empty_user_list_returns_empty_data(client):
    res = client.get('/users/')
    assert json.loads(res.data) == {
        "status": "success",
        "data": []
    }
    assert res.status_code == 200

@pytest.mark.parametrize('url', ['/books/1', '/users/1'])
def test_get_404(client, url):
    res = client.get(url)
    assert res.status_code == 404
    assert json.loads(res.data) == {'status': 'Resource not found'}

@pytest.mark.parametrize('url', ['/books/1', '/users/1', '/users/wishlist/1'])
def test_update_404(client, url):
    data = {"data": 'not relevant for this test.'}
    res = client.put(url, data=data)
    assert res.status_code == 404
    assert json.loads(res.data) == {'status': 'Resource not found'}


@pytest.mark.parametrize('url', ['/books/1', '/users/1', '/users/wishlist/1'])
def test_delete_404(client, url):
    res = client.delete(url)
    assert res.status_code == 404
    assert json.loads(res.data) == {'status': 'Resource not found'}


def test_create_book(client):
    data = {
        'title': 'Neverwhere', 'author': 'Neil Gaiman', 'isbn': '9780380973637', 'date_of_publication': '1996-09-16 00:00:00'
    }
    res = client.post('/books/', data=data)
    loaded_data = json.loads(res.data)
    verify_model(loaded_data['data'], data, 'book')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 


def test_error_on_creation_of_duplicate_book(client):
    data = {
        'title': 'Neverwhere', 'author': 'Neil Gaiman', 'isbn': '9780380973637', 'date_of_publication': '1996-09-16 00:00:00'
    }
    res = client.post('/books/', data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Resource already exists'}
    assert res.status_code == 400

def test_create_user(client):
    data = {
        'first_name': 'John', 'last_name': 'Smith', 'email': 'john_smith@generic.email', 'password': 'a_very_secure_password'
    }
    res = client.post('/users/', data=data)
    loaded_data = json.loads(res.data)
    data['wishlist'] = []
    verify_model(loaded_data['data'], data, 'user')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 


def test_error_on_creation_of_duplicate_user(client):
    data = {
        'first_name': 'John', 'last_name': 'Smith', 'email': 'john_smith@generic.email', 'password': 'a_very_secure_password'
    }
    res = client.post('/users/', data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Resource already exists'}
    assert res.status_code == 400

def test_get_user(client, sample_user):
    res = client.get(f"/users/{sample_user['data']['id']}")
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_user)
    del clone['data']['id']
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 


def test_update_user_proper_auth(client, sample_user):
    data = {
        'new_first_name': 'Steve', 'new_last_name': 'Williams', 'new_email': 'stevesnewemail@generic.email', 'new_password': 'p4$$VV0RD','password': 'p4$$VV0RD'
    }
    res = client.put(f"/users/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    sample_user['data']['email'] = 'stevesnewemail@generic.email'
    clone = deepcopy(sample_user)
    del clone['data']['id']
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 



def test_update_user_improper_auth(client, sample_user):
    data = {
        'new_first_name': 'Steve', 'new_last_name': 'Williams', 'new_email': 'stevesnewemail@generic.email', 'new_password': 'p4$$VV0RD','password': 'wrong_password'
    }
    res = client.put(f"/users/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Failed authentication. Password incorrect'}
    assert res.status_code == 400

def test_update_book(client, sample_book):
    data = {
        'new_title': 'An updated book name', 'new_author': 'V. E. Schwab', 'new_isbn': '0765376466', 'new_date_of_publication': '2016-01-19 00:00:00'
    }
    res = client.put(f"/books/{sample_book['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    sample_book['data']['title'] = 'An updated book name'
    clone = deepcopy(sample_book)
    del clone['data']['id']
    verify_model(loaded_data['data'], clone['data'], 'book')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 



def test_add_to_wishlist_proper_auth(client, sample_user, sample_book):
    data = {
        'book_id': sample_book['data']['id'], 'password': 'p4$$VV0RD'
    }
    res = client.put(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_user)
    del clone['data']['id']
    book_clone = deepcopy(sample_book)
    book_clone['data']['id']
    clone['data']['wishlist'].append(book_clone['data'])
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 


def test_add_to_wishlist_improper_auth(client, sample_user, sample_book):
    data = {
        'book_id': sample_book['data']['id'], 'password': 'wrong_password'
    }
    res = client.put(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Failed authentication. Password incorrect'}
    assert res.status_code == 400

def test_update_wishlist_book_already_there(client, sample_user, sample_book):
    data = {
        'book_id': sample_book['data']['id'], 'password': 'p4$$VV0RD'
    }
    res = client.put(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_user)
    del clone['data']['id']
    book_clone = deepcopy(sample_book)
    book_clone['data']['id']
    clone['data']['wishlist'].append(book_clone['data'])
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 


def test_book_list_returns_data(client):
    res = client.get('/books/')
    loaded_data = json.loads(res.data)
    assert len(loaded_data['data']) == 2
    for i in loaded_data['data']:
        assert i['type'] == 'book'
    assert res.status_code == 200

def test_user_list_returns_data(client):
    res = client.get('/users/')
    loaded_data = json.loads(res.data)
    assert len(loaded_data['data']) == 2
    for i in loaded_data['data']:
        assert i['type'] == 'user'
    assert res.status_code == 200


def test_update_wishlist_book_does_not_exist(client, sample_user):
    data = {
        'book_id': '1', 'password': 'p4$$VV0RD'
    }
    res = client.put(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    assert res.status_code == 404
    assert json.loads(res.data) == {'status': 'Resource not found'}


def test_delete_wishlisted_book_fails(client, sample_book):
    res = client.delete(f"/books/{sample_book['data']['id']}")
    loaded_data = json.loads(res.data)
    assert loaded_data == {"status": "Cannot remove due to book existing in at least one user's wishlist"}
    assert res.status_code == 400

def test_remove_book_from_wishlist_improper_auth(client, sample_user, sample_book):
    data = {
        'book_id': sample_book['data']['id'], 'password': 'wrong_password'
    }
    res = client.delete(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Failed authentication. Password incorrect'}
    assert res.status_code == 400


def test_remove_book_from_wishlist_proper_auth(client, sample_user, sample_book):
    data = {
        'book_id': sample_book['data']['id'], 'password': 'p4$$VV0RD'
    }
    res = client.delete(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_user)
    del clone['data']['id']
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 


def test_remove_book_that_is_not_in_wishlist(client, sample_user, sample_book):
    data = {
        'book_id': '1', 'password': 'p4$$VV0RD'
    }
    res = client.delete(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Resource not found'}
    assert res.status_code == 404


def delete_user_improper_auth(client, sample_user):
    data = {
        'password': 'wrong_password'
    }
    res = client.delete(f"/users/{sample_user['data']['id']}")
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Failed authentication. Password incorrect'}
    assert res.status_code == 400

def test_delete_user_proper_auth(client, sample_user):
    data = {
        'password': 'p4$$VV0RD'
    }
    res = client.delete(f"/users/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {"status": "success"}
    assert res.status_code == 200
    check_for_user_res = client.get(f"/users/{sample_user['data']['id']}")
    check_for_user_loaded_data = json.loads(check_for_user_res.data)
    assert check_for_user_loaded_data == {'status': 'Resource not found'}


def test_delete_book(client, sample_book):
    res = client.delete(f"/books/{sample_book['data']['id']}")
    loaded_data = json.loads(res.data)
    assert loaded_data == {"status": "success"}
    assert res.status_code == 200
    check_for_book_res = client.get(f"/books/{sample_book['data']['id']}")
    check_for_book_loaded_data = json.loads(check_for_book_res.data)
    assert check_for_book_loaded_data == {'status': 'Resource not found'}
    loaded_data = json.loads(res.data)



def test_code_fails_gracefully_with_bad_request(client):
    data = {'not_a_valid_key': 'not_a_valid_value'}
    res = client.post("/users/", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'One or more of the fields was invalid or missing.'}
    assert res.status_code == 400

