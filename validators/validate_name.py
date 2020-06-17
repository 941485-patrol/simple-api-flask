from wtforms.validators import ValidationError
from app import db

class ValidateName():
    def __init__(self, model, column, subj):
        self.model = model
        self.column = column
        self.subj = subj
        self.msg = '{} is already taken.'.format(self.subj)

    def __call__(self, form, field):
        idformdata=form.id.data
        fielddata=field.data
        count=db.session.query(db.func.count(self.model.id)).scalar()
        if idformdata=='':
            fields=self.model.query.filter(self.model.listing[self.column].ilike(fielddata)).first()
        else:
            fields=self.model.query.filter(self.model.id!=idformdata,self.model.listing[self.column].ilike(fielddata)).first()
        if fields is not None:
            fields = fields.serialize()
            if fields.get(self.column).lower() == fielddata.lower():
                raise ValidationError(self.msg)