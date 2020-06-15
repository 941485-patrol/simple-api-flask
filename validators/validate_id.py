from flask import (request)
from wtforms.validators import ValidationError

class ValidateById():
    def __init__(self, model, column, subj):
        self.subj = subj
        self.column = column
        self.model = model
        self.msg = 'Wrong {} id.'.format(self.subj)

    def __call__(self, form, field):
        try:
            if form.id.data == '':
                data=self.model.query.filter_by(id=field.data).first()
                if not data:
                    raise ValidationError(self.msg)
            else:
                path=str(request.path).split('/')
                int(field.data)
                if self.column == 'id':
                    if path[3] != field.data:
                        raise ValidationError(self.msg)                    
                data=self.model.query.filter_by(id=field.data).first()
                if not data:
                    raise ValidationError(self.msg)
        except ValueError as e:
            raise ValidationError(self.msg)