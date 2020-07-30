from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Regexp, InputRequired, Length, EqualTo
from models import User
from validators import ValidateName, ValidatePass, ValidateById, IsIdNumber, IsIdPathValid, stripData

class RegisterForm(FlaskForm):
    id=HiddenField(
        label='id', 
        validators=[
            stripData, 
            IsIdNumber(idData='field-data'), 
            IsIdPathValid(), 
            ValidateById(User,'User',pk=True)
            ])
    username=StringField(
        label='username', 
        validators=[
            stripData, 
            DataRequired(), 
            Length(min=8,max=16,message='Username must be between %(min)d and %(max)d characters.'), 
            IsIdNumber(idData='form-data'), IsIdPathValid(), ValidateName(User,'username','Username')
            ])
    password=PasswordField(
        label='password', 
        validators=[
            stripData, 
            DataRequired(), 
            Length(min=8,max=16,message='Password must be between %(min)d and %(max)d characters.'),
            EqualTo('confirm', message='Passwords must match.'),
            IsIdNumber(idData='form-data'), 
            IsIdPathValid(),
            ValidatePass()
        ])
    confirm = PasswordField(
        label='confirm',
        validators=[
            stripData,
            DataRequired(),
        ])
