from models import Employee, Occupation
from sqlalchemy.orm import load_only
from wtforms.validators import ValidationError

# Class-based 
class ValidateName():
    def __init__(self, model, column, subj):
        self.model = model
        self.column = column
        self.subj = subj
        self.msg = '{} is already taken.'.format(self.subj)
    
    def __call__(self, form, field): 
        if form.id.data=='':
            if self.column=='name':
                fields=self.model.query.filter_by(name=field.data).first()
                if fields is None:
                    pass
                elif fields.name.lower() == field.data.lower():
                    raise ValidationError(self.msg)
            if self.column=='description':
                fields=self.model.query.filter_by(description=field.data).first()
                if fields is None:
                    pass
                elif fields.description.lower() == field.data.lower() and fields is not None:
                    raise ValidationError(self.msg)
            if self.column=='email':
                fields=self.model.query.filter_by(email=field.data).first()
                if fields is None:
                    pass
                elif fields.email.lower() == field.data.lower() and fields is not None:
                    raise ValidationError(self.msg)
        else:
            valid_id = self.model.query.get(form.id.data)
            if not valid_id:
                raise ValidationError('Id associated with this field is not correct.')
            if self.column=='name':
                fields=self.model.query.filter(self.model.id!=form.id.data,self.model.name==field.data).first()
                if fields is None:
                    pass
                else:
                    raise ValidationError(self.msg)
            if self.column=='description':
                fields=self.model.query.filter(self.model.id!=form.id.data,self.model.description==field.data).first()
                if fields is None:
                    pass
                else:
                    raise ValidationError(self.msg)
            if self.column=='email':
                fields=self.model.query.filter(self.model.id!=form.id.data,self.model.email==field.data).first()
                if fields is None:
                    pass
                else:
                    raise ValidationError(self.msg)

# Function-based
# def validate_name(form, field):
#     employees=Employee.query.order_by(Employee.id).options(load_only('name')).all()
#     empList=[]
#     for employee in employees:
#         empList.append(employee.name)
#     for x in empList:
#         if x.lower() == field.data.lower():
#             raise ValidationError('Name is already taken.')

# Other form
# if form.id.data == '':
#     fields=self.model.query.order_by(self.model.id).options(load_only(self.column)).all()
# else:
#     fields=self.model.query.filter(self.model.id!=form.id.data).order_by(self.model.id).all()
#     fieldList=[]
#     for fld in fields:
#         if self.column == 'name':
#             fieldList.append(fld.name)
#         if self.column == 'description':
#             fieldList.append(fld.description)
#         if self.column == 'email':
#             fieldList.append(fld.email)
#     for x in fieldList:
#         if x.lower() == field.data.lower():
#             raise ValidationError(self.msg)