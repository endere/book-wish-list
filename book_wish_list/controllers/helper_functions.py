"""Helper functions used by one or both of the main controllers. Kept here to keep code clean."""
from sqlalchemy.exc import IntegrityError
from tables.user import User
from flask import request
from werkzeug.exceptions import BadRequestKeyError


def api_response(data, status, code=200):
    """
    Return json response to user.

    If the data is a list, return a response of the json of all objects in that list.
    If the data is a json blob, return that as the data.
    If the data is None, just return the given status.
    """
    if type(data) == list:
        return {"status": status, "data": [obj.json for obj in data]}, code
    elif data:
        return {"status": status, "data": data}, code
    else:
        return {"status": status}, code


def error_wrapper(f):
    """Decorator that handles errors in code and turns them into appropriate responses."""
    def _wrapper(*args, **kwargs):
        """
        Call function and return response.

        An AttributeError means that a resource was not found.
        An IntegrityError means that sqlalchemy tried to put a value in the database whose unique key already exists (email for users and isbn for books.)
        A BadRequestKeyError means that either not all of the required request parameters were present, or one or more of them were ill-formatted.
        A ValueError means that a request was made to remove an existing book from an existing wishlist, but that book is not IN that wishlist.
        """
        try:
            res = f(*args, **kwargs)
        except AttributeError:
            return api_response(None, 'Resource not found', 404)
        except IntegrityError:
            return api_response(None, 'Resource already exists', 400)
        except BadRequestKeyError:
            return api_response(None, 'One or more of the fields was invalid or missing', 400)
        except ValueError:
            return api_response(None, 'Book exists but is not in wishlist', 400)
        return res
    return _wrapper


def auth_wrapper(f):
    """Decorator ensures User is authorized to perform editing commands."""
    def _wrapper(obj, id):
        """
        Check that the password is the proper password for User of the given id, then continue to perform function.

        Else, return authentication error.
        Return not found error if user is not found, handled by error_wrapper.
        """
        user = User.query.filter_by(id=id).first()
        if not user:
            raise AttributeError
        if int(id) == user.id and request.values['password'] == user.password:
            return f(obj, user)
        else:
            return api_response(None, "Failed authentication. Password incorrect", 400)
    return _wrapper
