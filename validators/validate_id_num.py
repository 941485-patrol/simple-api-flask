from wtforms.validators import StopValidation
import re

class IsIdNumber():
    def __init__(self, idData=None):
        self.idData = idData
        self.msg = 'Invalid Id number.'

    def __call__(self, form, field):
        if self.idData == 'form-data':
            string=form.id.data
        if self.idData == 'field-data':
            string=field.data
        if string == '0':
            string='A'
        pattern = re.compile('^$|^[0-9]+$')
        matched =  pattern.match(string)
        if not matched:
            raise StopValidation(self.msg)