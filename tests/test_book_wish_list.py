"""Test file for book_wish_list app."""

import json
import pytest
from test_helpers import verify_model
from copy import deepcopy


def test_empty_book_list_returns_empty_data(client):
    """Show that database is empty of books and that '/books/' returns empty list."""
    res = client.get('/books/')
    assert json.loads(res.data) == {
        "status": "success",
        "data": []
    }
    assert res.status_code == 200


def test_empty_user_list_returns_empty_data(client):
    """Show that database is empty of users and that '/users/' returns empty list."""
    res = client.get('/users/')
    assert json.loads(res.data) == {
        "status": "success",
        "data": []
    }
    assert res.status_code == 200


@pytest.mark.parametrize('url', ['/books/1', '/users/1'])
def test_get_404(client, url):
    """Assert that 404s are properly returned for get paths."""
    res = client.get(url)
    assert res.status_code == 404
    assert json.loads(res.data) == {'status': 'Resource not found'}


@pytest.mark.parametrize('url', ['/books/1', '/users/1', '/users/wishlist/1'])
def test_update_404(client, url):
    """Assert that 404s are properly returned for put paths."""
    data = {"data": 'not relevant for this test.'}
    res = client.put(url, data=data)
    assert res.status_code == 404
    assert json.loads(res.data) == {'status': 'Resource not found'}


@pytest.mark.parametrize('url', ['/books/1', '/users/1', '/users/wishlist/1'])
def test_delete_404(client, url):
    """Assert that 404s are properly returned for delete paths."""
    res = client.delete(url)
    assert res.status_code == 404
    assert json.loads(res.data) == {'status': 'Resource not found'}


def test_create_book(client):
    """
    Create a book in the database and ensure it presents the proper data.

    Note: This is called before the sample_book fixture, ensuring that the post and return is valid before that fixture is used to assist with other tests.
    """
    data = {
        'title': 'Neverwhere', 'author': 'Neil Gaiman', 'isbn': '9780380973637', 'date_of_publication': '1996-09-16 00:00:00'
    }
    res = client.post('/books/', data=data)
    loaded_data = json.loads(res.data)
    verify_model(loaded_data['data'], data, 'book')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 


def test_error_on_creation_of_duplicate_book(client):
    """Assert that proper 400 error is returned when a book with the same isbn is posted."""
    data = {
        'title': 'Neverwhere', 'author': 'Neil Gaiman', 'isbn': '9780380973637', 'date_of_publication': '1996-09-16 00:00:00'
    }
    res = client.post('/books/', data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Resource already exists'}
    assert res.status_code == 400

def test_create_user(client):
    """
    Create a user in the database and ensure it presents the proper data.

    Note: This is called before the sample_user fixture, ensuring that the post and return is valid before that fixture is used to assist with other tests.
    """
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
    """Assert that proper 400 error is returned when a user with the same email is posted."""
    data = {
        'first_name': 'John', 'last_name': 'Smith', 'email': 'john_smith@generic.email', 'password': 'a_very_secure_password'
    }
    res = client.post('/users/', data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Resource already exists'}
    assert res.status_code == 400

def test_get_user(client, sample_user):
    """User sample_user fixture to assert that the results of the get are the same as the user that was posted."""
    res = client.get(f"/users/{sample_user['data']['id']}")
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_user)
    del clone['data']['id']
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 


def test_update_user_proper_auth(client, sample_user):
    """Assert that the sample_user can be updated, provided correct password."""
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
    """
    Assert that the sample user cannot be updated when incorrect password is supplied.

    Note: the 'new_password' is the correct one, but the code checks the 'password' field for authentication. This is so users may update their passwords.
    """
    data = {
        'new_first_name': 'Steve', 'new_last_name': 'Williams', 'new_email': 'stevesnewemail@generic.email', 'new_password': 'p4$$VV0RD','password': 'wrong_password'
    }
    res = client.put(f"/users/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Failed authentication. Password incorrect'}
    assert res.status_code == 400


def test_get_book(client, sample_book):
    """User sample_book fixture to assert that the results of the get are the same as the book that was posted."""
    res = client.get(f"/books/{sample_book['data']['id']}")
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_book)
    del clone['data']['id']
    verify_model(loaded_data['data'], clone['data'], 'book')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 

def test_update_book(client, sample_book):
    """Assert the sample book can be updated."""
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
    """
    Add the sample_book to the sample_user's wishlist with proper authentication.

    Assert that it is indeed shown as there.
    """
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
    """Assert that the sample user's wishlist cannot be updated when incorrect password is supplied."""
    data = {
        'book_id': sample_book['data']['id'], 'password': 'wrong_password'
    }
    res = client.put(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Failed authentication. Password incorrect'}
    assert res.status_code == 400

def test_update_wishlist_book_already_there(client, sample_user, sample_book):
    """Assert that updating a wishlist with a book that is already there does not add to the wishlist."""
    data = {
        'book_id': sample_book['data']['id'], 'password': 'p4$$VV0RD'
    }
    res = client.put(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_user)
    del clone['data']['id']
    book_clone = deepcopy(sample_book)
    del book_clone['data']['id']
    clone['data']['wishlist'].append(book_clone['data'])
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert len(loaded_data['data']['wishlist']) == 1
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 

def test_update_wishlist_with_second_book(client, sample_user, sample_book):
    """Assert that updating a wishlist with a second book that is not there adds a second to the wishlist, and the user is returned with both books shown in wishlist."""
    second_book_data = {
        'title': 'Theft of Swords', 'author': 'Micheal J Sullivan', 'isbn': '0316187747', 'date_of_publication': '2011-11-23 00:00:00'
    }
    second_book_res = client.post(f"/books/", data=second_book_data)
    second_book_loaded_data = json.loads(second_book_res.data)
    data = {
        'book_id': second_book_loaded_data['data']['id'], 'password': 'p4$$VV0RD'
    }
    res = client.put(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_user)
    del clone['data']['id']
    book_clone = deepcopy(sample_book)
    del book_clone['data']['id']
    clone['data']['wishlist'].append(book_clone['data'])
    clone['data']['wishlist'].append(second_book_data)
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert res.status_code == 200
    assert len(loaded_data['data']['wishlist']) == 2
    assert loaded_data['status'] == 'success' 

def test_book_can_be_added_to_multiple_wishlists(client, sample_book):
    """
    Create a new user, and add sample book to wishlist. Assert that this book can exist in that wishlist as well. 

    Then delete user as cleanup, else book will not be able to be deleted later. As this function is not for testing delete, no asserts are used there.
    """
    new_user_data = {
        'first_name': 'Persony', 'last_name': 'Mcpersonface', 'email': 'person@person.face', 'password': 'absolutely_a_real_user'
    }
    new_user_res = client.post('/users/', data=new_user_data)
    new_user_loaded_data = json.loads(new_user_res.data)
    data = {
        'book_id': sample_book['data']['id'], 'password': 'absolutely_a_real_user'
    }
    res = client.put(f"/users/wishlist/{new_user_loaded_data['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    book_clone = deepcopy(sample_book)
    del book_clone['data']['id']
    new_user_data['wishlist'] = [book_clone['data']]
    verify_model(loaded_data['data'], new_user_data, 'user')
    assert len(loaded_data['data']['wishlist']) == 1
    assert res.status_code == 200
    assert loaded_data['status'] == 'success' 
    delete_data = {
        'password': 'absolutely_a_real_user'
    }
    client.delete(f"/users/{new_user_loaded_data['data']['id']}", data={'password': 'absolutely_a_real_user'})


def test_book_list_returns_data(client):
    """Assert that calling the list of books now includes three books."""
    res = client.get('/books/')
    loaded_data = json.loads(res.data)
    assert len(loaded_data['data']) == 3
    for i in loaded_data['data']:
        assert i['type'] == 'book'
    assert res.status_code == 200

def test_user_list_returns_data(client):
    """Assert that calling the list of users now includes two users."""
    res = client.get('/users/')
    loaded_data = json.loads(res.data)
    assert len(loaded_data['data']) == 2
    for i in loaded_data['data']:
        assert i['type'] == 'user'
    assert res.status_code == 200


def test_update_wishlist_book_does_not_exist(client, sample_user):
    """Assert that trying to put a book that does not exist into a wishlist returns a 404 error."""
    data = {
        'book_id': '1', 'password': 'p4$$VV0RD'
    }
    res = client.put(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    assert res.status_code == 404
    assert json.loads(res.data) == {'status': 'Resource not found'}


def test_delete_wishlisted_book_fails(client, sample_book):
    """Assert that trying to delete a book that is wishlisted fails and returns an appropriate error."""
    res = client.delete(f"/books/{sample_book['data']['id']}")
    loaded_data = json.loads(res.data)
    assert loaded_data == {"status": "Cannot remove due to book existing in at least one user's wishlist"}
    assert res.status_code == 400

def test_remove_book_from_wishlist_improper_auth(client, sample_user, sample_book):
    """Assert that trying to remove a book from a wishlist with improper auth fails and returns proper error."""
    data = {
        'book_id': sample_book['data']['id'], 'password': 'wrong_password'
    }
    res = client.delete(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Failed authentication. Password incorrect'}
    assert res.status_code == 400


def test_remove_book_from_wishlist_proper_auth(client, sample_user, sample_book):
    """
    User proper authentication to remove a book from sample user's wishlist.

    Then assert that success message is given, and that the returned user has the proper amount of books in wishlist (just one now). 
    """
    data = {
        'book_id': sample_book['data']['id'], 'password': 'p4$$VV0RD'
    }
    res = client.delete(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    clone = deepcopy(sample_user)
    del clone['data']['id']
    assert len(loaded_data['data']['wishlist']) == 1
    verify_model(loaded_data['data'], clone['data'], 'user')
    assert res.status_code == 200
    assert loaded_data['status'] == 'success'



def test_remove_book_that_does_not_exist_from_wishlist(client, sample_user, sample_book):
    """Assert that trying to remove nonexistant book from wishlist returns 404."""
    data = {
        'book_id': '1', 'password': 'p4$$VV0RD'
    }
    res = client.delete(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Resource not found'}
    assert res.status_code == 404

def test_remove_book_that_is_not_in_wishlist(client, sample_user, sample_book):
    """Assert that trying to remove existing book from existing wishlist that it is not in"""
    data = {
        'book_id': sample_book['data']['id'], 'password': 'p4$$VV0RD'
    }
    res = client.delete(f"/users/wishlist/{sample_user['data']['id']}", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Book exists but is not in wishlist'}
    assert res.status_code == 400



def delete_user_improper_auth(client, sample_user):
    """Assert that trying to delete a user with improper authentication fails with proper error."""
    data = {
        'password': 'wrong_password'
    }
    res = client.delete(f"/users/{sample_user['data']['id']}")
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'Failed authentication. Password incorrect'}
    assert res.status_code == 400

def test_delete_user_proper_auth(client, sample_user):
    """Assert that deleting a user with proper authentication removes the user. Then a get request to that user's id returns a 404."""
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
    """Assert that deleting a book removes the book. Then a get request to that book's id returns a 404."""
    res = client.delete(f"/books/{sample_book['data']['id']}")
    loaded_data = json.loads(res.data)
    assert loaded_data == {"status": "success"}
    assert res.status_code == 200
    check_for_book_res = client.get(f"/books/{sample_book['data']['id']}")
    check_for_book_loaded_data = json.loads(check_for_book_res.data)
    assert check_for_book_loaded_data == {'status': 'Resource not found'}
    loaded_data = json.loads(res.data)



def test_code_fails_gracefully_with_bad_request(client):
    """Test that a request to the api with invalid data returns a proper 400 error response."""
    data = {'not_a_valid_key': 'not_a_valid_value'}
    res = client.post("/users/", data=data)
    loaded_data = json.loads(res.data)
    assert loaded_data == {'status': 'One or more of the fields was invalid or missing'}
    assert res.status_code == 400
