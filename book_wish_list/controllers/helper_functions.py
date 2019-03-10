from sqlalchemy.exc import IntegrityError
from tables.user import User
from flask import request



def api_response(model, status):
    if type(model) == list:
        return {"status": status, "data": [obj.json for obj in model]}
    if model:
        return {"status": status, "model": model.json}
    else:
        return {"status": status}

def error_wrapper(f):
    """Decorator that parses errors and response codes from controller response."""
    def _wrapper(*args, **kwargs):
        """."""
        try:
            res = f(*args, **kwargs)
        except AttributeError:
            return {'Error': 'Resource not found'}, 404
        except IntegrityError:
            return {'Error': 'Resource already exists'}, 400
        return res
    return _wrapper

def auth_wrapper(f):
    """Decorator that parses errors and response codes from controller response."""
    def _wrapper(obj, id):
        """."""
        user = User.query.filter_by(id=id).first()
        if int(id) == user.id and request.values['password'] == user.password:
            return f(obj, user)
        else:
            return api_response(None, "Failed authentication. Password incorrect")
    return _wrapper