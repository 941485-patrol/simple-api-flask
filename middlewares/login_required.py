from flask import (g,abort,jsonify)
import functools

def login_required(func):
    def decorator(*args, **kwargs):
        if g.user is None:
            abort(401)
        else:
            return func(*args,**kwargs)
    return decorator 

# def login_required(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         if g.user is None:
#             abort(404)
#         return func(*args,**kwargs)
#     return wrapper