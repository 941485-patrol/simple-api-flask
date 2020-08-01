from flask.helpers import make_response
from flask import (request)

def responser(*args):
    res = make_response(*args)
    sess_cookie = request.cookies.get('session',None)
    if sess_cookie is not None:
        # res.set_cookie('session',value=sess_cookie,samesite='None',secure=True,httponly=True,path='/')
        res.headers['Set-Cookie'] = 'session={}; SameSite=None; Secure; HttpOnly; path=/'.format(sess_cookie)
        return res