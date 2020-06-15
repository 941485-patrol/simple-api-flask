from models import Employee, Occupation
from sqlalchemy.orm import load_only
from wtforms.validators import ValidationError
from sqlalchemy.exc import DataError, InternalError
from flask import (request)

class ValidateName():
    def __init__(self, model, column, subj):
        self.model = model
        self.column = column
        self.subj = subj
        self.msg = '{} is already taken.'.format(self.subj)
        self.msg2 = 'Id associated with this field is invalid.'
    def __call__(self, form, field): 
        if form.id.data=='':
            if self.column=='name':
                fields=self.model.query.filter(self.model.name.ilike(field.data)).first()
                if fields is None:
                    pass
                elif fields.name.lower() == field.data.lower():
                    raise ValidationError(self.msg)
            if self.column=='description':
                fields=self.model.query.filter(self.model.description.ilike(field.data)).first()
                if fields is None:
                    pass
                elif fields.description.lower() == field.data.lower() and fields is not None:
                    raise ValidationError(self.msg)
            if self.column=='email':
                fields=self.model.query.filter(self.model.email.ilike(field.data)).first()
                if fields is None:
                    pass
                elif fields.email.lower() == field.data.lower() and fields is not None:
                    raise ValidationError(self.msg)
        else:
            path=str(request.path).split('/')
            if path[3] != form.id.data:
                raise ValidationError(self.msg2)
            if self.column=='name':
                fields=self.model.query.filter(self.model.id!=form.id.data,self.model.name.ilike(field.data)).first()
                if fields is None:
                    pass
                elif fields.name.lower() == field.data.lower():
                    raise ValidationError(self.msg)
            if self.column=='description':
                fields=self.model.query.filter(self.model.id!=form.id.data,self.model.description.ilike(field.data)).first()
                if fields is None:
                    pass
                elif fields.description.lower() == field.data.lower():
                    raise ValidationError(self.msg)
            if self.column=='email':
                fields=self.model.query.filter(self.model.id!=form.id.data,self.model.email.ilike(field.data)).first()
                if fields is None:
                    pass
                elif fields.email.lower() == field.data.lower() and fields is not None:
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