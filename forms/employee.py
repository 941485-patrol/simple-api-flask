from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Regexp, ValidationError
from validators import ValidateName, ValidateById, CheckId, stripper
from models import Employee, Occupation

class EmployeeForm(FlaskForm):
    id=HiddenField(label='id', validators=[stripper, CheckId('Employee','int','pk'), ValidateById(Employee,'id','Employee')])
    name=StringField(label='name', validators=[DataRequired(), stripper, CheckId('Employee','str','pk'), ValidateName(Employee,'name','Name')])
    email=EmailField(label='email', validators=[DataRequired(), stripper, CheckId('Employee','str','pk'), Email(message='Invalid Email.'), ValidateName(Employee,'email','E-mail')])
    occupations_id=StringField(label='occupations_id', validators=[DataRequired(), stripper, CheckId('Job','int'), ValidateById(Occupation,'occupations_id','Job')])