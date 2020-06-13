from models.occupation import Occupation
from sqlalchemy.orm import load_only
from wtforms.validators import ValidationError

class ValidateById():
    def __init__(self, model, column, subj):
        self.subj = subj
        self.column = column
        self.model = model
        self.msg = 'Wrong {} id.'.format(self.subj)

    def __call__(self, form, field):
        if form.id.data == '':
            if self.column =='occupations_id':
                data=self.model.query.filter(self.model.occupations_id==field.data).first()
                if not data:
                    raise ValidationError(self.msg)
        else:
            if self.column == 'occupations_id':
                data=self.model.query.filter_by(occupations_id=field.data).first()
                if not data:
                    raise ValidationError(self.msg)
            if self.column == 'id':
                data=self.model.query.filter_by(id=field.data).first()
                if not data:
                    raise ValidationError(self.msg)