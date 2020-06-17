from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Regexp, ValidationError
from validators import ValidateName, ValidateById, IsIdNumber, IsIdPathValid, stripData
from models import Employee, Occupation

class EmployeeForm(FlaskForm):
    id=HiddenField(label='id', validators=[stripData, IsIdNumber(idData='field-data'), IsIdPathValid(), ValidateById(Employee,'Employee',pk=True)])
    name=StringField(label='name', validators=[DataRequired(), stripData, IsIdNumber(idData='form-data'), IsIdPathValid(), ValidateName(Employee,'name','Name')])
    email=EmailField(label='email', validators=[DataRequired(), stripData, IsIdNumber(idData='form-data'), IsIdPathValid(), Email(message='Invalid Email.'), ValidateName(Employee,'email','E-mail')])
    occupations_id=StringField(label='occupations_id', validators=[DataRequired(), stripData, IsIdNumber(idData='field-data'), ValidateById(Occupation,'Job',pk=False)])