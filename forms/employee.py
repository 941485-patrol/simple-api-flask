from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, NoneOf, ValidationError
from validators import ValidateName, ValidateById, stripper
from models.employee import Employee

class EmployeeForm(FlaskForm):
    id=HiddenField(label='id', validators=[ValidateById(Employee,'id','Employee'), stripper])
    name=StringField(label='name', validators=[DataRequired(), ValidateName(Employee,'name','Name'), stripper])
    email=EmailField(label='email', validators=[DataRequired(), Email(message='Invalid Email.'), ValidateName(Employee,'email','E-mail'), stripper])
    occupations_id=StringField(label='occupations_id', validators=[DataRequired(), ValidateById(Employee,'occupations_id','Job'), stripper])