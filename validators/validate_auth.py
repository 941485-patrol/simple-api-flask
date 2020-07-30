from wtforms.validators import StopValidation
from models import User
from werkzeug.security import check_password_hash
from flask import (session)

class ValidateAuth():
    def __init__(self):
        self.msg1 ='Wrong credentials.'
        self.msg2 = 'Wrong password.'

    def __call__(self, form, field):
        username = field.data
        password = form.password.data
        if len(password) == 0:
            raise StopValidation(message=self.msg1)
        isUserExists=User.query.filter_by(username=username).first()
        if isUserExists:
            pwhash=isUserExists.password
            isPassCorrect=check_password_hash(pwhash,password)
            if isPassCorrect:
                session.clear()
                session['user_id'] = isUserExists.id
            else:
                raise StopValidation(message=self.msg2)
        else:
            raise StopValidation(message=self.msg1)