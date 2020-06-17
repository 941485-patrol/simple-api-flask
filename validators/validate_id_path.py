from wtforms.validators import StopValidation
from flask import (request)

class IsIdPathValid():
    def __init__(self):
        self.msg = 'Invalid Id path'

    def __call__(self, form, field):
        path=str(request.path).split('/')
        string=form.id.data
        if len(path)<4:
            if string!='':
              raise StopValidation(self.msg)
        else:
            if string=='':
                raise StopValidation(self.msg)
            if path[3] != string:
                raise StopValidation(self.msg)