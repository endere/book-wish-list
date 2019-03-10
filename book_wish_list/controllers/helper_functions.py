from sqlalchemy.exc import IntegrityError
from tables.user import User
from flask import request
from werkzeug.exceptions import BadRequestKeyError

def api_response(data, status, code=200):
    if type(data) == list:
        return {"status": status, "data": [obj.json for obj in data]}, code
    elif data:
        return {"status": status, "data": data}, code
    else:
        return {"status": status}, code

def error_wrapper(f):
    """Decorator that parses errors and response codes from controller response."""
    def _wrapper(*args, **kwargs):
        """."""
        try:
            res = f(*args, **kwargs)
        except AttributeError:
            return api_response(None, 'Resource not found', 404)
        except IntegrityError:
            return api_response(None, 'Resource already exists', 400)
        except BadRequestKeyError:
            return api_response(None, 'One or more of the fields was invalid or missing.', 400)
        return res
    return _wrapper

def auth_wrapper(f):
    """Decorator that parses errors and response codes from controller response."""
    def _wrapper(obj, id):
        """."""
        user = User.query.filter_by(id=id).first()
        if not user:
            raise AttributeError
        if int(id) == user.id and request.values['password'] == user.password:
            return f(obj, user)
        else:
            return api_response(None, "Failed authentication. Password incorrect", 400)
    return _wrapper