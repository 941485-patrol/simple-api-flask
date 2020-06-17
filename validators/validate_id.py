from wtforms.validators import ValidationError

class ValidateById():
    def __init__(self, model, column, subj):
        self.subj = subj
        self.column = column
        self.model = model
        self.msg = 'Wrong {} id.'.format(self.subj)

    def __call__(self, form, field):
        if form.id.data == '':
            if self.column != 'id':
                data=self.model.query.filter_by(id=field.data).first()
                if data is None:
                    raise ValidationError(self.msg)
        else:
            data=self.model.query.filter_by(id=field.data).first()
            if data is None:
                raise ValidationError(self.msg)