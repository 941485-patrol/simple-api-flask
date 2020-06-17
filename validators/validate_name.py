from models import Employee, Occupation
from sqlalchemy.orm import load_only
from wtforms.validators import ValidationError
from sqlalchemy.exc import DataError, InternalError

class ValidateName():
    def __init__(self, model, column, subj):
        self.model = model
        self.column = column
        self.subj = subj
        self.msg = '{} is already taken.'.format(self.subj)

    def __call__(self, form, field):
        if form.id.data=='':
            fields=self.model.query.filter(self.model.listing[self.column].ilike(field.data)).first()
        else:
            fields=self.model.query.filter(self.model.id!=form.id.data,self.model.listing[self.column].ilike(field.data)).first()
        if fields is not None:
            fields = fields.serialize()
            if fields.get(self.column).lower() == field.data.lower():
                raise ValidationError(self.msg)