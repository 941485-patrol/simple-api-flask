from wtforms.validators import ValidationError

class ValidateById():
    def __init__(self, model, subj, pk=False):
        self.subj = subj
        self.model = model
        self.pk = pk
        self.msg = 'Wrong {} id.'.format(self.subj)

    def __call__(self, form, field):
        string=field.data
        if string=='' and self.pk==True:
            return string
        elif string=='' and self.pk==False:
            raise ValidationError(self.msg)
        data=self.model.query.filter_by(id=string).first()
        if data is None:
            raise ValidationError(self.msg)