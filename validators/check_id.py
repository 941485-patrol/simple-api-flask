from wtforms.validators import StopValidation
from flask import(request)
import re
class CheckId():
    def __init__(self, subj, typeof, pk=None):
        self.subj = subj
        self.typeof = typeof
        self.pk = pk
        self.msg = '{} id is invalid.'.format(self.subj)

    def __call__(self, form, field):
        path=str(request.path).split('/')
        if self.pk is not None:
            if len(path)<4:
                if form.id.data != '':
                    raise StopValidation(self.msg)
                else:
                    return field.data
            else:
                if path[3] != form.id.data:
                    raise StopValidation(self.msg) 
        if self.typeof == 'int':
            string = field.data
        elif self.typeof == 'str':
            string = form.id.data
        pattern = re.compile('^[0-9]+$')
        matched =  pattern.match(string)
        if not matched:
            raise StopValidation(self.msg)